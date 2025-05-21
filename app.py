import argparse
import os
import sys
import uuid
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
import wfdb
from loguru import logger
from scipy.signal import correlate, welch
from scipy.stats import gaussian_kde


def ensure_dir(directory: str) -> None:
    """Creează directorul dacă nu există."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def save_plot(fig, filename: str, save: bool = True) -> None:
    """Salvează figura în directorul grafice/. Suprascrie dacă există."""
    if not save:
        return
    ensure_dir('grafice')
    out_path = os.path.join('grafice', filename)
    fig.savefig(out_path)
    logger.info(f"Grafic salvat: {out_path}")


def ecdf(data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Calculează ECDF pentru un vector de date."""
    x = np.sort(data)
    y = np.arange(1, len(x) + 1) / len(x)
    return x, y


def plot_ecg_signal(signal: np.ndarray, fs: int, record_name: str, save: bool = True, show: bool = True) -> None:
    """Plotează semnalul ECG."""
    t = np.arange(len(signal)) / fs
    fig = plt.figure(figsize=(12, 4))
    plt.plot(t, signal, color='blue')
    plt.title(f'Semnalul ECG (canal {record_name})')
    plt.xlabel('Timp (secunde)')
    plt.ylabel('Amplitude (mV)')
    plt.grid(True)
    plt.tight_layout()
    save_plot(fig, 'ecg_signal.png', save)
    if show:
        plt.show()
    plt.close()


def plot_ecdf(signal: np.ndarray, save: bool = True, show: bool = True) -> None:
    """Plotează ECDF pentru semnal."""
    x_ecdf, y_ecdf = ecdf(signal)
    fig = plt.figure(figsize=(8, 4))
    plt.plot(x_ecdf, y_ecdf, marker='.', linestyle='none')
    plt.title('Funcția de repartiție empirică (ECDF)')
    plt.xlabel('Amplitudine (mV)')
    plt.ylabel('F(x)')
    plt.grid(True)
    plt.tight_layout()
    save_plot(fig, 'ecdf.png', save)
    if show:
        plt.show()
    plt.close()


def plot_pdf(signal: np.ndarray, save: bool = True, show: bool = True) -> None:
    """Plotează PDF estimat cu histograma și KDE."""
    kde = gaussian_kde(signal)
    x_vals = np.linspace(np.min(signal), np.max(signal), 1000)
    fig = plt.figure(figsize=(8, 4))
    plt.hist(signal, bins=30, density=True, alpha=0.5, label='Histograma (PDF)')
    plt.plot(x_vals, kde(x_vals), color='red', label='KDE (PDF)')
    plt.title('Densitatea de probabilitate (PDF)')
    plt.xlabel('Amplitudine (mV)')
    plt.ylabel('Densitate de probabilitate')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    save_plot(fig, 'pdf.png', save)
    if show:
        plt.show()
    plt.close()


def plot_autocorrelation(signal: np.ndarray, save: bool = True, show: bool = True) -> None:
    """Plotează funcția de autocorelatie."""
    acorr = correlate(signal - np.mean(signal), signal - np.mean(signal), mode='full')
    acorr = acorr[acorr.size // 2:]
    lags = np.arange(0, len(acorr))
    fig = plt.figure(figsize=(10, 4))
    plt.plot(lags, acorr)
    plt.title('Funcția de autocorelatie a semnalului ECG')
    plt.xlabel('Lag (număr de eșantioane)')
    plt.ylabel('Autocorelatie')
    plt.grid(True)
    plt.tight_layout()
    save_plot(fig, 'autocorrelation.png', save)
    if show:
        plt.show()
    plt.close()


def plot_psd(signal: np.ndarray, fs: int, save: bool = True, show: bool = True) -> None:
    """Plotează densitatea spectrală de putere (PSD)."""
    f, Pxx = welch(signal, fs=fs, nperseg=2048)
    fig = plt.figure(figsize=(10, 4))
    plt.semilogy(f, Pxx)
    plt.title('Densitatea spectrală de putere (PSD) a semnalului ECG')
    plt.xlabel('Frecvență (Hz)')
    plt.ylabel('Densitate de putere (V^2/Hz)')
    plt.grid(True)
    plt.tight_layout()
    save_plot(fig, 'psd.png', save)
    if show:
        plt.show()
    plt.close()


def print_statistics(signal: np.ndarray, record_name: str) -> None:
    """Afișează statistici de bază pentru semnal."""
    mean_value = np.mean(signal)
    variance_value = np.var(signal)
    dispersion_value = np.std(signal)
    logger.info(f"Media semnalului ECG ({record_name}) este: {mean_value:.4f}")
    logger.info(f"Varianta semnalului ECG ({record_name}) este: {variance_value:.4f}")
    logger.info(f"Dispersia (deviația standard) semnalului ECG ({record_name}) este: {dispersion_value:.4f}")


def load_ecg_channel(record_path: str, record_id: str, channel: int = 0, start: int = 10000, end: int = 15000) -> Tuple[np.ndarray, str]:
    """Încarcă un segment dintr-un canal ECG dintr-un fișier PhysioNet."""
    record_name = record_path + record_id
    try:
        record = wfdb.rdrecord(record_name)
    except Exception as e:
        logger.error(f"Eroare la citirea fișierului {record_name}: {e}")
        sys.exit(1)
    signal = record.p_signal[:, channel]
    return signal[start:end], record_name


def main():
    default_path = 'physionet.org/files/chfdb/1.0.0/'
    default_record = 'chf01'
    default_channel = 0
    default_start = 10000
    default_end = 15000
    default_fs = 250
    default_save = True

    parser = argparse.ArgumentParser(description="Analiză și ploturi pentru semnal ECG din PhysioNet.")
    parser.add_argument('--path', type=str, default=default_path, help='Calea către directorul cu fișiere PhysioNet')
    parser.add_argument('--record', type=str, default=default_record, help='ID-ul fișierului de analizat (ex: chf01)')
    parser.add_argument('--channel', type=int, default=default_channel, help='Canalul ECG de analizat (default: 0)')
    parser.add_argument('--start', type=int, default=default_start, help='Indexul de start pentru segmentul analizat')
    parser.add_argument('--end', type=int, default=default_end, help='Indexul de final pentru segmentul analizat')
    parser.add_argument('--fs', type=int, default=default_fs, help='Frecvența de eșantionare (Hz)')
    parser.add_argument('--save', type=lambda x: (str(x).lower() == 'true'), default=default_save, help='Salvează graficele în directorul grafice/ (default: True)')
    args = parser.parse_args()

    channel_sample, record_name = load_ecg_channel(
        args.path, args.record, args.channel, args.start, args.end
    )

    print_statistics(channel_sample, record_name)
    plot_ecg_signal(channel_sample, args.fs, record_name, save=args.save, show=True)
    plot_ecdf(channel_sample, save=args.save, show=True)
    plot_pdf(channel_sample, save=args.save, show=True)
    plot_autocorrelation(channel_sample, save=args.save, show=True)
    plot_psd(channel_sample, args.fs, save=args.save, show=True)


if __name__ == "__main__":
    main()
