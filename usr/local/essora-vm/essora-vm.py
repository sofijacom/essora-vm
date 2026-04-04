#!/usr/bin/env python3
# Essora VM - QEMU Virtual Machine Manager
# GTK3 + Python3 — Essora Linux
# Author: josejp2424
# License: GPL-3.0
# Copyright (C) 2025 josejp2424
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gtk, Gdk, GLib, Pango

import os
import sys
import json
import subprocess
import shlex
import glob
import locale
import shutil
import signal
import time

CONFIG_DIR  = os.path.expanduser("~/.config/essora-vm")
VMS_FILE    = os.path.join(CONFIG_DIR, "vms.json")
PIDS_FILE   = os.path.join(CONFIG_DIR, "pids.json")
os.makedirs(CONFIG_DIR, exist_ok=True)

TRANSLATIONS = {
    "en": {
        "title":        "Essora VM",
        "my_vms":       "My Virtual Machines",
        "new_vm":       "+ New VM",
        "settings":     "⚙ Settings",
        "close":        "✕ Close",
        "start":        "▶  Start",
        "stop":         "■  Stop",
        "restart":      "↺  Restart",
        "delete":       "🗑  Delete",
        "cpu_label":    "CPU:",
        "ram_label":    "RAM:",
        "disk_label":   "Disk:",
        "cores":        "cores",
        "iso_label":    "ISO Image:",
        "cpu_cfg":      "CPU:",
        "ram_cfg":      "Memory RAM:",
        "graphics":     "Graphics:",
        "network":      "Network:",
        "no_vm":        "No VM selected",
        "no_vm_sub":    "Select a VM from the left panel\nor create a new one.",
        "confirm_del":  "Delete Virtual Machine",
        "confirm_del2": "Are you sure you want to delete",
        "cancel":       "Cancel",
        "delete_btn":   "Delete",
        "vm_running":   "Running",
        "vm_stopped":   "Stopped",
        "new_vm_title": "New Virtual Machine",
        "vm_name":      "VM Name:",
        "disk_path":    "Disk Image Path:",
        "disk_size":    "Disk Size (GB):",
        "browse":       "Browse…",
        "create_disk":  "Create disk",
        "create":       "Create VM",
        "gb":           "GB",
        "language":     "Language",
        "err_no_name":  "VM name cannot be empty.",
        "err_no_disk":  "Disk image path cannot be empty.",
        "err_dup":      "A VM with that name already exists.",
        "settings_title": "Global Settings",
        "qemu_path":    "QEMU binary path:",
        "save":         "Save",
        "saved":        "Settings saved.",
        "arch_label":   "Architecture:",
        "no_qemu":      "QEMU not found. Please install QEMU.",
        "disk_created": "Disk image created.",
        "stopped_ok":   "VM stopped.",
        "started_ok":   "VM started.",
        "restarted_ok": "VM restarted.",
        "about":         "About",
        "about_title":   "About Essora VM",
        "about_author":  "Author",
        "about_dev":     "Essora Developer",
        "about_version": "Version",
        "about_license": "License",
        "minimize":      "Minimize",
        "maximize":      "Maximize",
    },
    "es": {
        "title":        "Essora VM",
        "my_vms":       "Mis Máquinas Virtuales",
        "new_vm":       "+ Nueva VM",
        "settings":     "⚙ Configuración",
        "close":        "✕ Cerrar",
        "start":        "▶  Iniciar",
        "stop":         "■  Detener",
        "restart":      "↺  Reiniciar",
        "delete":       "🗑  Eliminar",
        "cpu_label":    "CPU:",
        "ram_label":    "RAM:",
        "disk_label":   "Disco:",
        "cores":        "núcleos",
        "iso_label":    "Imagen ISO:",
        "cpu_cfg":      "CPU:",
        "ram_cfg":      "Memoria RAM:",
        "graphics":     "Gráficos:",
        "network":      "Red:",
        "no_vm":        "Sin VM seleccionada",
        "no_vm_sub":    "Selecciona una VM del panel izquierdo\no crea una nueva.",
        "confirm_del":  "Eliminar Máquina Virtual",
        "confirm_del2": "¿Está seguro de eliminar",
        "cancel":       "Cancelar",
        "delete_btn":   "Eliminar",
        "vm_running":   "En ejecución",
        "vm_stopped":   "Detenida",
        "new_vm_title": "Nueva Máquina Virtual",
        "vm_name":      "Nombre de VM:",
        "disk_path":    "Ruta de imagen de disco:",
        "disk_size":    "Tamaño del disco (GB):",
        "browse":       "Explorar…",
        "create_disk":  "Crear disco",
        "create":       "Crear VM",
        "gb":           "GB",
        "language":     "Idioma",
        "err_no_name":  "El nombre de la VM no puede estar vacío.",
        "err_no_disk":  "La ruta de imagen de disco no puede estar vacía.",
        "err_dup":      "Ya existe una VM con ese nombre.",
        "settings_title": "Configuración Global",
        "qemu_path":    "Ruta del binario QEMU:",
        "save":         "Guardar",
        "saved":        "Configuración guardada.",
        "arch_label":   "Arquitectura:",
        "no_qemu":      "QEMU no encontrado. Por favor instale QEMU.",
        "disk_created": "Imagen de disco creada.",
        "stopped_ok":   "VM detenida.",
        "started_ok":   "VM iniciada.",
        "restarted_ok": "VM reiniciada.",
    },
    "ar": {
        "title":        "Essora VM",
        "my_vms":       "أجهزتي الافتراضية",
        "new_vm":       "+ جهاز جديد",
        "settings":     "⚙ الإعدادات",
        "close":        "✕ إغلاق",
        "start":        "▶  تشغيل",
        "stop":         "■  إيقاف",
        "restart":      "↺  إعادة تشغيل",
        "delete":       "🗑  حذف",
        "cpu_label":    "المعالج:",
        "ram_label":    "الذاكرة:",
        "disk_label":   "القرص:",
        "cores":        "أنوية",
        "iso_label":    "صورة ISO:",
        "cpu_cfg":      "المعالج:",
        "ram_cfg":      "الذاكرة RAM:",
        "graphics":     "الرسوميات:",
        "network":      "الشبكة:",
        "no_vm":        "لم يتم اختيار جهاز افتراضي",
        "no_vm_sub":    "اختر جهازاً من اللوحة اليسرى\nأو أنشئ جهازاً جديداً.",
        "confirm_del":  "حذف الجهاز الافتراضي",
        "confirm_del2": "هل أنت متأكد من حذف",
        "cancel":       "إلغاء",
        "delete_btn":   "حذف",
        "vm_running":   "قيد التشغيل",
        "vm_stopped":   "متوقف",
        "new_vm_title": "جهاز افتراضي جديد",
        "vm_name":      "اسم الجهاز:",
        "disk_path":    "مسار صورة القرص:",
        "disk_size":    "حجم القرص (GB):",
        "browse":       "استعراض…",
        "create_disk":  "إنشاء قرص",
        "create":       "إنشاء الجهاز",
        "gb":           "GB",
        "language":     "اللغة",
        "err_no_name":  "اسم الجهاز الافتراضي لا يمكن أن يكون فارغاً.",
        "err_no_disk":  "مسار صورة القرص لا يمكن أن يكون فارغاً.",
        "err_dup":      "يوجد جهاز افتراضي بهذا الاسم بالفعل.",
        "settings_title": "الإعدادات العامة",
        "qemu_path":    "مسار ملف QEMU:",
        "save":         "حفظ",
        "saved":        "تم حفظ الإعدادات.",
        "arch_label":   "المعمارية:",
        "no_qemu":      "QEMU غير موجود. يرجى تثبيت QEMU.",
        "disk_created": "تم إنشاء صورة القرص.",
        "stopped_ok":   "تم إيقاف الجهاز الافتراضي.",
        "started_ok":   "تم تشغيل الجهاز الافتراضي.",
        "restarted_ok": "تمت إعادة تشغيل الجهاز الافتراضي.",
    },
    "ca": {
        "title":"Essora VM","my_vms":"Les meves màquines virtuals","new_vm":"+ Nova VM",
        "settings":"⚙ Configuració","close":"✕ Tanca","start":"▶  Inicia","stop":"■  Atura",
        "restart":"↺  Reinicia","delete":"🗑  Elimina","cpu_label":"CPU:","ram_label":"RAM:",
        "disk_label":"Disc:","cores":"nuclis","iso_label":"Imatge ISO:","cpu_cfg":"CPU:",
        "ram_cfg":"Memòria RAM:","graphics":"Gràfics:","network":"Xarxa:",
        "no_vm":"Cap VM seleccionada","no_vm_sub":"Selecciona una VM del panell esquerre\no crea'n una de nova.",
        "confirm_del":"Elimina la màquina virtual","confirm_del2":"Segur que voleu eliminar",
        "cancel":"Cancel·la","delete_btn":"Elimina","vm_running":"En execució","vm_stopped":"Aturada",
        "new_vm_title":"Nova màquina virtual","vm_name":"Nom de la VM:","disk_path":"Ruta de la imatge:",
        "disk_size":"Mida del disc (GB):","browse":"Navega…","create_disk":"Crea disc","create":"Crea VM",
        "gb":"GB","language":"Idioma","err_no_name":"El nom de la VM no pot estar buit.",
        "err_no_disk":"La ruta de la imatge no pot estar buida.","err_dup":"Ja existeix una VM amb aquest nom.",
        "settings_title":"Configuració global","qemu_path":"Ruta del binari QEMU:","save":"Desa","saved":"Configuració desada.",
        "arch_label":"Arquitectura:","no_qemu":"QEMU no trobat. Instal·leu QEMU.","disk_created":"Imatge de disc creada.",
        "stopped_ok":"VM aturada.","started_ok":"VM iniciada.","restarted_ok":"VM reiniciada.",
    },
    "de": {
        "title":"Essora VM","my_vms":"Meine virtuellen Maschinen","new_vm":"+ Neue VM",
        "settings":"⚙ Einstellungen","close":"✕ Schließen","start":"▶  Starten","stop":"■  Stoppen",
        "restart":"↺  Neustart","delete":"🗑  Löschen","cpu_label":"CPU:","ram_label":"RAM:",
        "disk_label":"Disk:","cores":"Kerne","iso_label":"ISO-Abbild:","cpu_cfg":"CPU:",
        "ram_cfg":"Arbeitsspeicher:","graphics":"Grafik:","network":"Netzwerk:",
        "no_vm":"Keine VM ausgewählt","no_vm_sub":"VM im linken Panel auswählen\noder eine neue erstellen.",
        "confirm_del":"Virtuelle Maschine löschen","confirm_del2":"Wirklich löschen?",
        "cancel":"Abbrechen","delete_btn":"Löschen","vm_running":"Läuft","vm_stopped":"Gestoppt",
        "new_vm_title":"Neue virtuelle Maschine","vm_name":"VM-Name:","disk_path":"Disk-Image-Pfad:",
        "disk_size":"Disk-Größe (GB):","browse":"Durchsuchen…","create_disk":"Disk erstellen","create":"VM erstellen",
        "gb":"GB","language":"Sprache","err_no_name":"VM-Name darf nicht leer sein.",
        "err_no_disk":"Disk-Image-Pfad darf nicht leer sein.","err_dup":"Eine VM mit diesem Namen existiert bereits.",
        "settings_title":"Globale Einstellungen","qemu_path":"QEMU-Binärpfad:","save":"Speichern","saved":"Einstellungen gespeichert.",
        "arch_label":"Architektur:","no_qemu":"QEMU nicht gefunden. Bitte QEMU installieren.",
        "disk_created":"Disk-Image erstellt.","stopped_ok":"VM gestoppt.","started_ok":"VM gestartet.","restarted_ok":"VM neugestartet.",
    },
    "fr": {
        "title":"Essora VM","my_vms":"Mes machines virtuelles","new_vm":"+ Nouvelle VM",
        "settings":"⚙ Paramètres","close":"✕ Fermer","start":"▶  Démarrer","stop":"■  Arrêter",
        "restart":"↺  Redémarrer","delete":"🗑  Supprimer","cpu_label":"CPU:","ram_label":"RAM:",
        "disk_label":"Disque:","cores":"cœurs","iso_label":"Image ISO:","cpu_cfg":"CPU:",
        "ram_cfg":"Mémoire RAM:","graphics":"Graphiques:","network":"Réseau:",
        "no_vm":"Aucune VM sélectionnée","no_vm_sub":"Sélectionnez une VM dans le panneau gauche\nou créez-en une nouvelle.",
        "confirm_del":"Supprimer la machine virtuelle","confirm_del2":"Voulez-vous vraiment supprimer",
        "cancel":"Annuler","delete_btn":"Supprimer","vm_running":"En cours","vm_stopped":"Arrêtée",
        "new_vm_title":"Nouvelle machine virtuelle","vm_name":"Nom de la VM:","disk_path":"Chemin de l'image disque:",
        "disk_size":"Taille du disque (Go):","browse":"Parcourir…","create_disk":"Créer le disque","create":"Créer la VM",
        "gb":"Go","language":"Langue","err_no_name":"Le nom de la VM ne peut pas être vide.",
        "err_no_disk":"Le chemin de l'image disque ne peut pas être vide.","err_dup":"Une VM avec ce nom existe déjà.",
        "settings_title":"Paramètres globaux","qemu_path":"Chemin du binaire QEMU:","save":"Enregistrer","saved":"Paramètres enregistrés.",
        "arch_label":"Architecture:","no_qemu":"QEMU introuvable. Veuillez installer QEMU.",
        "disk_created":"Image disque créée.","stopped_ok":"VM arrêtée.","started_ok":"VM démarrée.","restarted_ok":"VM redémarrée.",
    },
    "it": {
        "title":"Essora VM","my_vms":"Le mie macchine virtuali","new_vm":"+ Nuova VM",
        "settings":"⚙ Impostazioni","close":"✕ Chiudi","start":"▶  Avvia","stop":"■  Ferma",
        "restart":"↺  Riavvia","delete":"🗑  Elimina","cpu_label":"CPU:","ram_label":"RAM:",
        "disk_label":"Disco:","cores":"core","iso_label":"Immagine ISO:","cpu_cfg":"CPU:",
        "ram_cfg":"Memoria RAM:","graphics":"Grafica:","network":"Rete:",
        "no_vm":"Nessuna VM selezionata","no_vm_sub":"Seleziona una VM dal pannello sinistro\no creane una nuova.",
        "confirm_del":"Elimina macchina virtuale","confirm_del2":"Eliminare davvero",
        "cancel":"Annulla","delete_btn":"Elimina","vm_running":"In esecuzione","vm_stopped":"Fermata",
        "new_vm_title":"Nuova macchina virtuale","vm_name":"Nome VM:","disk_path":"Percorso immagine disco:",
        "disk_size":"Dimensione disco (GB):","browse":"Sfoglia…","create_disk":"Crea disco","create":"Crea VM",
        "gb":"GB","language":"Lingua","err_no_name":"Il nome della VM non può essere vuoto.",
        "err_no_disk":"Il percorso dell'immagine non può essere vuoto.","err_dup":"Una VM con questo nome esiste già.",
        "settings_title":"Impostazioni globali","qemu_path":"Percorso binario QEMU:","save":"Salva","saved":"Impostazioni salvate.",
        "arch_label":"Architettura:","no_qemu":"QEMU non trovato. Installa QEMU.",
        "disk_created":"Immagine disco creata.","stopped_ok":"VM fermata.","started_ok":"VM avviata.","restarted_ok":"VM riavviata.",
    },
    "pt": {
        "title":"Essora VM","my_vms":"Minhas Máquinas Virtuais","new_vm":"+ Nova VM",
        "settings":"⚙ Configurações","close":"✕ Fechar","start":"▶  Iniciar","stop":"■  Parar",
        "restart":"↺  Reiniciar","delete":"🗑  Excluir","cpu_label":"CPU:","ram_label":"RAM:",
        "disk_label":"Disco:","cores":"núcleos","iso_label":"Imagem ISO:","cpu_cfg":"CPU:",
        "ram_cfg":"Memória RAM:","graphics":"Gráficos:","network":"Rede:",
        "no_vm":"Nenhuma VM selecionada","no_vm_sub":"Selecione uma VM no painel esquerdo\nou crie uma nova.",
        "confirm_del":"Excluir Máquina Virtual","confirm_del2":"Tem certeza que deseja excluir",
        "cancel":"Cancelar","delete_btn":"Excluir","vm_running":"Em execução","vm_stopped":"Parada",
        "new_vm_title":"Nova Máquina Virtual","vm_name":"Nome da VM:","disk_path":"Caminho da imagem de disco:",
        "disk_size":"Tamanho do disco (GB):","browse":"Procurar…","create_disk":"Criar disco","create":"Criar VM",
        "gb":"GB","language":"Idioma","err_no_name":"O nome da VM não pode estar vazio.",
        "err_no_disk":"O caminho da imagem de disco não pode estar vazio.","err_dup":"Já existe uma VM com esse nome.",
        "settings_title":"Configurações Globais","qemu_path":"Caminho do binário QEMU:","save":"Salvar","saved":"Configurações salvas.",
        "arch_label":"Arquitetura:","no_qemu":"QEMU não encontrado. Instale o QEMU.",
        "disk_created":"Imagem de disco criada.","stopped_ok":"VM parada.","started_ok":"VM iniciada.","restarted_ok":"VM reiniciada.",
    },
    "ja": {
        "title":"Essora VM","my_vms":"仮想マシン一覧","new_vm":"+ 新規VM",
        "settings":"⚙ 設定","close":"✕ 閉じる","start":"▶  起動","stop":"■  停止",
        "restart":"↺  再起動","delete":"🗑  削除","cpu_label":"CPU:","ram_label":"RAM:",
        "disk_label":"ディスク:","cores":"コア","iso_label":"ISO イメージ:","cpu_cfg":"CPU:",
        "ram_cfg":"メモリ RAM:","graphics":"グラフィックス:","network":"ネットワーク:",
        "no_vm":"VM 未選択","no_vm_sub":"左パネルから VM を選択するか\n新規作成してください。",
        "confirm_del":"仮想マシンの削除","confirm_del2":"削除してよいですか？",
        "cancel":"キャンセル","delete_btn":"削除","vm_running":"実行中","vm_stopped":"停止中",
        "new_vm_title":"新規仮想マシン","vm_name":"VM 名:","disk_path":"ディスクイメージのパス:",
        "disk_size":"ディスクサイズ (GB):","browse":"参照…","create_disk":"ディスク作成","create":"VM 作成",
        "gb":"GB","language":"言語","err_no_name":"VM 名を入力してください。",
        "err_no_disk":"ディスクイメージのパスを入力してください。","err_dup":"その名前の VM は既に存在します。",
        "settings_title":"グローバル設定","qemu_path":"QEMU バイナリのパス:","save":"保存","saved":"設定を保存しました。",
        "arch_label":"アーキテクチャ:","no_qemu":"QEMU が見つかりません。QEMU をインストールしてください。",
        "disk_created":"ディスクイメージを作成しました。","stopped_ok":"VM を停止しました。","started_ok":"VM を起動しました。","restarted_ok":"VM を再起動しました。",
    },
    "hu": {
        "title":"Essora VM","my_vms":"Virtuális gépeim","new_vm":"+ Új VM",
        "settings":"⚙ Beállítások","close":"✕ Bezárás","start":"▶  Indítás","stop":"■  Leállítás",
        "restart":"↺  Újraindítás","delete":"🗑  Törlés","cpu_label":"CPU:","ram_label":"RAM:",
        "disk_label":"Lemez:","cores":"mag","iso_label":"ISO-kép:","cpu_cfg":"CPU:",
        "ram_cfg":"Memória RAM:","graphics":"Grafika:","network":"Hálózat:",
        "no_vm":"Nincs VM kiválasztva","no_vm_sub":"Válasszon VM-et a bal panelből\nvagy hozzon létre újat.",
        "confirm_del":"Virtuális gép törlése","confirm_del2":"Biztosan törli?",
        "cancel":"Mégse","delete_btn":"Törlés","vm_running":"Fut","vm_stopped":"Leállítva",
        "new_vm_title":"Új virtuális gép","vm_name":"VM neve:","disk_path":"Lemez-kép elérési útja:",
        "disk_size":"Lemez mérete (GB):","browse":"Tallózás…","create_disk":"Lemez létrehozása","create":"VM létrehozása",
        "gb":"GB","language":"Nyelv","err_no_name":"A VM neve nem lehet üres.",
        "err_no_disk":"A lemez-kép elérési útja nem lehet üres.","err_dup":"Már létezik ilyen nevű VM.",
        "settings_title":"Globális beállítások","qemu_path":"QEMU bináris elérési útja:","save":"Mentés","saved":"Beállítások mentve.",
        "arch_label":"Architektúra:","no_qemu":"QEMU nem található. Kérjük, telepítse a QEMU-t.",
        "disk_created":"Lemez-kép létrehozva.","stopped_ok":"VM leállítva.","started_ok":"VM elindítva.","restarted_ok":"VM újraindítva.",
    },
    "ru": {
        "title":"Essora VM","my_vms":"Мои виртуальные машины","new_vm":"+ Новая ВМ",
        "settings":"⚙ Настройки","close":"✕ Закрыть","start":"▶  Запустить","stop":"■  Остановить",
        "restart":"↺  Перезапустить","delete":"🗑  Удалить","cpu_label":"ЦП:","ram_label":"ОЗУ:",
        "disk_label":"Диск:","cores":"ядра","iso_label":"ISO-образ:","cpu_cfg":"ЦП:",
        "ram_cfg":"Память RAM:","graphics":"Графика:","network":"Сеть:",
        "no_vm":"ВМ не выбрана","no_vm_sub":"Выберите ВМ на левой панели\nили создайте новую.",
        "confirm_del":"Удаление виртуальной машины","confirm_del2":"Вы уверены, что хотите удалить",
        "cancel":"Отмена","delete_btn":"Удалить","vm_running":"Работает","vm_stopped":"Остановлена",
        "new_vm_title":"Новая виртуальная машина","vm_name":"Имя ВМ:","disk_path":"Путь к образу диска:",
        "disk_size":"Размер диска (ГБ):","browse":"Обзор…","create_disk":"Создать диск","create":"Создать ВМ",
        "gb":"ГБ","language":"Язык","err_no_name":"Имя ВМ не может быть пустым.",
        "err_no_disk":"Путь к образу диска не может быть пустым.","err_dup":"ВМ с таким именем уже существует.",
        "settings_title":"Глобальные настройки","qemu_path":"Путь к бинарному файлу QEMU:","save":"Сохранить","saved":"Настройки сохранены.",
        "arch_label":"Архитектура:","no_qemu":"QEMU не найден. Пожалуйста, установите QEMU.",
        "disk_created":"Образ диска создан.","stopped_ok":"ВМ остановлена.","started_ok":"ВМ запущена.","restarted_ok":"ВМ перезапущена.",
    },
    "zh": {
        "title":"Essora VM","my_vms":"我的虚拟机","new_vm":"+ 新建虚拟机",
        "settings":"⚙ 设置","close":"✕ 关闭","start":"▶  启动","stop":"■  停止",
        "restart":"↺  重启","delete":"🗑  删除","cpu_label":"CPU：","ram_label":"内存：",
        "disk_label":"磁盘：","cores":"核心","iso_label":"ISO 镜像：","cpu_cfg":"CPU：",
        "ram_cfg":"内存 RAM：","graphics":"图形：","network":"网络：",
        "no_vm":"未选择虚拟机","no_vm_sub":"从左侧面板选择虚拟机\n或创建新的虚拟机。",
        "confirm_del":"删除虚拟机","confirm_del2":"确定要删除吗",
        "cancel":"取消","delete_btn":"删除","vm_running":"运行中","vm_stopped":"已停止",
        "new_vm_title":"新建虚拟机","vm_name":"虚拟机名称：","disk_path":"磁盘镜像路径：",
        "disk_size":"磁盘大小（GB）：","browse":"浏览…","create_disk":"创建磁盘","create":"创建虚拟机",
        "gb":"GB","language":"语言","err_no_name":"虚拟机名称不能为空。",
        "err_no_disk":"磁盘镜像路径不能为空。","err_dup":"已存在同名虚拟机。",
        "settings_title":"全局设置","qemu_path":"QEMU 二进制路径：","save":"保存","saved":"设置已保存。",
        "arch_label":"架构：","no_qemu":"未找到 QEMU，请安装 QEMU。",
        "disk_created":"磁盘镜像已创建。","stopped_ok":"虚拟机已停止。","started_ok":"虚拟机已启动。","restarted_ok":"虚拟机已重启。",
    },
}

LANGUAGE_NAMES = {
    "en":"English","ar":"العربية","ca":"Català","es":"Español","de":"Deutsch",
    "fr":"Français","it":"Italiano","pt":"Português","ja":"日本語",
    "hu":"Magyar","ru":"Русский","zh":"中文",
}

# SETTINGS

SETTINGS_FILE = os.path.join(CONFIG_DIR, "settings.json")

def load_settings():
    defaults = {"lang": "en", "qemu_bin": "/usr/bin/qemu-system-x86_64"}
    if os.path.isfile(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE) as f:
                d = json.load(f)
                defaults.update(d)
        except Exception:
            pass
    return defaults

def save_settings(d):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(d, f, indent=2)

def detect_lang():
    try:
        code = (locale.getdefaultlocale()[0] or "en")[:2].lower()
        return code if code in TRANSLATIONS else "en"
    except Exception:
        return "en"

def detect_qemu_bin():
    for b in glob.glob("/usr/bin/qemu-system-x86_64"):
        return b
    for b in glob.glob("/usr/bin/qemu-system-*"):
        return b
    return "qemu-system-x86_64"

#  VM DATA

def load_vms():
    if os.path.isfile(VMS_FILE):
        try:
            with open(VMS_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return []

def save_vms(vms):
    with open(VMS_FILE, "w") as f:
        json.dump(vms, f, indent=2)

def load_pids():
    if os.path.isfile(PIDS_FILE):
        try:
            with open(PIDS_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_pids(pids):
    with open(PIDS_FILE, "w") as f:
        json.dump(pids, f, indent=2)

def is_running(name, pids):
    pid = pids.get(name)
    if pid is None:
        return False
    try:
        os.kill(int(pid), 0)
        return True
    except (ProcessLookupError, PermissionError):
        return False

#  theme CSS

CSS = """
* { font-family: Cantarell, DejaVu Sans, sans-serif; }

window, .root-box { background-color: #1a1f2e; }

/* -- Header -- */
.header {
    background-color: #111827;
    border-bottom: 1px solid #2d3748;
    padding: 0 16px;
    min-height: 52px;
}
.header-title {
    color: #ffffff;
    font-size: 15pt;
    font-weight: bold;
}
.logo-leaf { color: #4ade80; font-size: 18pt; }

.btn-header {
    background-color: #1f2d40;
    color: #cbd5e0;
    border: 1px solid #2d4a6b;
    border-radius: 6px;
    padding: 5px 14px;
    font-size: 10pt;
}
.btn-header:hover { background-color: #2d3f55; color: #ffffff; }

.btn-new-vm {
    background-color: #22c55e;
    color: #052e16;
    border: none;
    border-radius: 6px;
    padding: 5px 14px;
    font-size: 10pt;
    font-weight: bold;
}
.btn-new-vm:hover { background-color: #16a34a; }

/* -- Sidebar -- */
.sidebar {
    background-color: #111827;
    border-right: 1px solid #1f2937;
    min-width: 210px;
}
.sidebar-title {
    color: #9ca3af;
    font-size: 9pt;
    font-weight: bold;
    padding: 14px 14px 6px 14px;
}

.vm-row {
    background-color: transparent;
    border-radius: 6px;
    padding: 8px 12px;
    margin: 2px 8px;
    color: #d1d5db;
    font-size: 10pt;
}
.vm-row:hover { background-color: #1f2937; }
.vm-row-selected {
    background-color: #14532d;
    color: #ffffff;
    font-weight: bold;
}

/* -- Main content -- */
.content-area { background-color: #1a1f2e; padding: 16px; }

.vm-name-title {
    color: #f9fafb;
    font-size: 14pt;
    font-weight: bold;
    padding-bottom: 8px;
}

/* Preview box */
.preview-box {
    background-color: #111827;
    border: 1px solid #374151;
    border-radius: 8px;
}
.preview-placeholder {
    color: #6b7280;
    font-size: 28pt;
}
.preview-placeholder-text {
    color: #6b7280;
    font-size: 10pt;
}

/* Info panel */
.info-label { color: #9ca3af; font-size: 10pt; }
.info-value { color: #f3f4f6; font-size: 10pt; font-weight: bold; }

/* Action buttons */
.btn-start {
    background-color: #22c55e;
    color: #052e16;
    border: none;
    border-radius: 6px;
    padding: 8px 20px;
    font-size: 10pt;
    font-weight: bold;
    min-width: 110px;
}
.btn-start:hover { background-color: #16a34a; }

.btn-stop {
    background-color: #374151;
    color: #d1d5db;
    border: 1px solid #4b5563;
    border-radius: 6px;
    padding: 8px 20px;
    font-size: 10pt;
    min-width: 110px;
}
.btn-stop:hover { background-color: #4b5563; color: #f9fafb; }

.btn-restart {
    background-color: #166534;
    color: #bbf7d0;
    border: 1px solid #16a34a;
    border-radius: 6px;
    padding: 8px 20px;
    font-size: 10pt;
    min-width: 110px;
}
.btn-restart:hover { background-color: #15803d; }

.btn-delete {
    background-color: #7f1d1d;
    color: #fecaca;
    border: 1px solid #b91c1c;
    border-radius: 6px;
    padding: 8px 20px;
    font-size: 10pt;
    min-width: 110px;
}
.btn-delete:hover { background-color: #991b1b; }

/* Config panel */
.config-area {
    background-color: #111827;
    border: 1px solid #1f2937;
    border-radius: 8px;
    padding: 14px;
    margin-top: 12px;
}
.config-label { color: #9ca3af; font-size: 10pt; }

entry {
    background-color: #1f2937;
    color: #f3f4f6;
    border: 1px solid #374151;
    border-radius: 5px;
    padding: 4px 8px;
    caret-color: #4ade80;
}
entry:focus { border-color: #22c55e; }

combobox button {
    background-color: #1f2937;
    color: #f3f4f6;
    border: 1px solid #374151;
    border-radius: 5px;
    padding: 3px 6px;
}

scale trough {
    background-color: #1f2937;
    border-radius: 4px;
    min-height: 6px;
}
scale highlight {
    background-color: #22c55e;
    border-radius: 4px;
}
scale slider {
    background-color: #4ade80;
    border-radius: 50%;
    min-width: 16px;
    min-height: 16px;
    border: none;
}

/* Empty state */
.empty-title { color: #6b7280; font-size: 13pt; font-weight: bold; }
.empty-sub   { color: #4b5563; font-size: 10pt; }

/* Status dot */
.dot-running { color: #22c55e; font-size: 14pt; }
.dot-stopped { color: #6b7280; font-size: 14pt; }

/* Status bar */
.statusbar {
    background-color: #0f172a;
    border-top: 1px solid #1f2937;
    color: #6b7280;
    font-size: 8pt;
    padding: 3px 12px;
}

label { color: #d1d5db; }

/* Language combo */
.lang-bar { background-color: #111827; padding: 2px 12px; }
.lang-bar label { color: #6b7280; font-size: 9pt; }
"""

def apply_css():
    provider = Gtk.CssProvider()
    provider.load_from_data(CSS.encode("utf-8"))
    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(), provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
    )

def add_class(widget, *classes):
    for c in classes:
        widget.get_style_context().add_class(c)

#  GRAPHICS and NETWORK OPTIONS

ARCH_OPTIONS     = [a.replace("/usr/bin/qemu-system-","")
                    for a in sorted(glob.glob("/usr/bin/qemu-system-*"))]
if not ARCH_OPTIONS:
    ARCH_OPTIONS = ["x86_64"]

#  NEW VM DIALOG

class NewVMDialog(Gtk.Dialog):
    def __init__(self, parent, tr, existing_names):
        super().__init__(title=tr["new_vm_title"], parent=parent,
                         flags=Gtk.DialogFlags.MODAL)
        self.set_default_size(480, 380)
        self.set_resizable(False)
        self.tr = tr
        self.existing_names = existing_names

        ca = self.get_content_area()
        ca.set_margin_start(20); ca.set_margin_end(20)
        ca.set_margin_top(16); ca.set_margin_bottom(8)
        ca.set_spacing(12)

        # VM Name
        row_name = Gtk.Box(spacing=8)
        lbl = Gtk.Label(label=tr["vm_name"]); lbl.set_width_chars(20); lbl.set_halign(Gtk.Align.START)
        self.name_entry = Gtk.Entry(); self.name_entry.set_hexpand(True)
        row_name.pack_start(lbl, False, False, 0)
        row_name.pack_start(self.name_entry, True, True, 0)
        ca.pack_start(row_name, False, False, 0)

        # Architecture
        row_arch = Gtk.Box(spacing=8)
        lbl2 = Gtk.Label(label=tr["arch_label"]); lbl2.set_width_chars(20); lbl2.set_halign(Gtk.Align.START)
        self.arch_combo = Gtk.ComboBoxText()
        for a in ARCH_OPTIONS:
            self.arch_combo.append_text(a)
        self.arch_combo.set_active(0)
        row_arch.pack_start(lbl2, False, False, 0)
        row_arch.pack_start(self.arch_combo, True, True, 0)
        ca.pack_start(row_arch, False, False, 0)

        # Disk size — disk will be auto-created at ~/.config/essora-vm/<name>.qcow2
        row_size = Gtk.Box(spacing=8)
        lbl4 = Gtk.Label(label=tr["disk_size"]); lbl4.set_width_chars(20); lbl4.set_halign(Gtk.Align.START)
        self.size_spin = Gtk.SpinButton.new_with_range(1, 2000, 1)
        self.size_spin.set_value(20)
        row_size.pack_start(lbl4, False, False, 0)
        row_size.pack_start(self.size_spin, False, False, 0)
        ca.pack_start(row_size, False, False, 0)

        # CPU / RAM
        row_cr = Gtk.Box(spacing=16)
        lbl5 = Gtk.Label(label=tr["cpu_cfg"]); lbl5.set_halign(Gtk.Align.START)
        self.cpu_spin = Gtk.SpinButton.new_with_range(1, 32, 1); self.cpu_spin.set_value(2)
        lbl6 = Gtk.Label(label=tr["ram_cfg"]); lbl6.set_halign(Gtk.Align.START)
        self.ram_spin = Gtk.SpinButton.new_with_range(128, 65536, 256); self.ram_spin.set_value(2048)
        row_cr.pack_start(lbl5, False, False, 0)
        row_cr.pack_start(self.cpu_spin, False, False, 0)
        row_cr.pack_start(lbl6, False, False, 0)
        row_cr.pack_start(self.ram_spin, False, False, 0)
        ca.pack_start(row_cr, False, False, 0)

        # error label
        self.err_label = Gtk.Label(label="")
        self.err_label.set_halign(Gtk.Align.START)
        ca.pack_start(self.err_label, False, False, 0)

        self.add_button(tr["cancel"], Gtk.ResponseType.CANCEL)
        btn_ok = self.add_button(tr["create"], Gtk.ResponseType.OK)
        add_class(btn_ok, "btn-new-vm")

        self.show_all()

    def get_vm(self):
        """Validate, create disk automatically, return VM dict or None."""
        tr = self.tr
        name = self.name_entry.get_text().strip()
        if not name:
            self.err_label.set_markup('<span color="#f87171">'+tr["err_no_name"]+'</span>')
            return None
        if name in self.existing_names:
            self.err_label.set_markup('<span color="#f87171">'+tr["err_dup"]+'</span>')
            return None
        # Auto disk path: ~/.config/essora-vm/<name>.qcow2
        disk = os.path.join(CONFIG_DIR, name + ".qcow2")
        size = int(self.size_spin.get_value())
        # Create the qcow2 disk image automatically
        try:
            subprocess.run(
                ["qemu-img", "create", "-f", "qcow2", disk, f"{size}G"],
                check=True, capture_output=True
            )
        except Exception as e:
            self.err_label.set_markup(f'<span color="#f87171">qemu-img: {e}</span>')
            return None
        arch = self.arch_combo.get_active_text() or "x86_64"

        # Smart defaults per architecture
        _needs_extra = ("riscv" in arch or "arm" in arch or "aarch" in arch or "mips" in arch or "ppc" in arch or "s390" in arch or "sparc" in arch)
        defaults = {}
        if "riscv64" in arch:
            defaults = {
                "machine":    "virt",
                "bios":       "/usr/lib/riscv64-linux-gnu/opensbi/generic/fw_dynamic.bin",
                "kernel":     "/usr/lib/u-boot/qemu-riscv64_smode/uboot.elf",
                "extra_args": "",
                "kvm":        False,
            }
        elif "aarch64" in arch or "arm64" in arch:
            defaults = {
                "machine":    "virt",
                "bios":       "/usr/share/qemu-efi-aarch64/QEMU_EFI.fd",
                "kernel":     "",
                "extra_args": "",
                "kvm":        False,
            }
        elif "arm" in arch:
            defaults = {
                "machine":    "virt",
                "bios":       "",
                "kernel":     "",
                "extra_args": "",
                "kvm":        False,
            }

        return {
            "name":      name,
            "arch":      arch,
            "disk":      disk,
            "disk_size": size,
            "cpu":       int(self.cpu_spin.get_value()),
            "ram":       int(self.ram_spin.get_value()),
            "iso":       "",
            "kvm":       defaults.get("kvm", True),
            "machine":   defaults.get("machine", ""),
            "bios":      defaults.get("bios", ""),
            "kernel":    defaults.get("kernel", ""),
            "extra_args":defaults.get("extra_args", ""),
        }

#  SETTINGS DIALOG

class SettingsDialog(Gtk.Dialog):
    def __init__(self, parent, tr, settings):
        super().__init__(title=tr["settings_title"], parent=parent,
                         flags=Gtk.DialogFlags.MODAL)
        self.set_default_size(420, 160)
        self.set_resizable(False)
        ca = self.get_content_area()
        ca.set_margin_start(20); ca.set_margin_end(20)
        ca.set_margin_top(16); ca.set_margin_bottom(8)
        ca.set_spacing(10)

        row = Gtk.Box(spacing=8)
        lbl = Gtk.Label(label=tr["qemu_path"]); lbl.set_width_chars(18); lbl.set_halign(Gtk.Align.START)
        self.qemu_entry = Gtk.Entry()
        self.qemu_entry.set_text(settings.get("qemu_bin", "/usr/bin/qemu-system-x86_64"))
        self.qemu_entry.set_hexpand(True)
        row.pack_start(lbl, False, False, 0)
        row.pack_start(self.qemu_entry, True, True, 0)
        ca.pack_start(row, False, False, 0)

        self.add_button(tr["cancel"], Gtk.ResponseType.CANCEL)
        self.add_button(tr["save"], Gtk.ResponseType.OK)
        self.show_all()

    def get_qemu_bin(self):
        return self.qemu_entry.get_text().strip()

#  MAIN WINDOW

class EssoraVM(Gtk.Window):

    def __init__(self):
        super().__init__()
        apply_css()

        self.settings = load_settings()
        lang = self.settings.get("lang") or detect_lang()
        if lang not in TRANSLATIONS:
            lang = "en"
        self.lang = lang
        self.tr = TRANSLATIONS[lang]

        self.vms  = load_vms()
        self.pids = load_pids()
        self.selected_vm = None       
        self.selected_idx = -1

        self.set_title("Essora VM")
        self.set_default_size(1060, 680)
        self.set_resizable(True)
        self.set_border_width(0)
        self.set_decorated(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", self._on_close)

        # Window icon 
        _logo_path = "/usr/local/essora-vm/logo-essora-vm.png"
        if os.path.isfile(_logo_path):
            try:
                from gi.repository import GdkPixbuf as _PB
                _icon = _PB.Pixbuf.new_from_file_at_scale(_logo_path, 48, 48, True)
                self.set_icon(_icon)
            except Exception:
                pass

        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        add_class(root, "root-box")
        self.add(root)

        root.pack_start(self._build_header(), False, False, 0)
        root.pack_start(self._build_lang_bar(), False, False, 0)

        body = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        body.set_hexpand(True); body.set_vexpand(True)
        root.pack_start(body, True, True, 0)

        self.sidebar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        add_class(self.sidebar_box, "sidebar")
        body.pack_start(self.sidebar_box, False, False, 0)

        self.main_stack = Gtk.Stack()
        self.main_stack.set_hexpand(True); self.main_stack.set_vexpand(True)
        body.pack_start(self.main_stack, True, True, 0)

        # Empty state
        self.empty_page = self._build_empty_page()
        self.main_stack.add_named(self.empty_page, "empty")

        # VM detail page (rebuilt on selection)
        self.detail_page = Gtk.Box()
        self.main_stack.add_named(self.detail_page, "detail")

        # Status bar row: About link (left) + status text (right)
        sbar_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        add_class(sbar_box, "statusbar")
        # Clickable "About" label
        self._about_lbl = Gtk.Label()
        self._about_lbl.set_markup('<span foreground="#4ade80" underline="single">About</span>')
        self._about_lbl.set_margin_start(8)
        self._about_lbl.set_tooltip_text("About Essora VM")
        evbox = Gtk.EventBox()
        evbox.add(self._about_lbl)
        evbox.connect("button-press-event", lambda w, e: self._on_about())
        evbox.connect("realize", lambda w: w.get_window().set_cursor(
            Gdk.Cursor.new_from_name(w.get_display(), "pointer")))
        sbar_box.pack_start(evbox, False, False, 0)
        self.statusbar = Gtk.Label(label="Essora VM  •  QEMU Frontend")
        self.statusbar.set_halign(Gtk.Align.END)
        self.statusbar.set_hexpand(True)
        self.statusbar.set_margin_end(8)
        sbar_box.pack_start(self.statusbar, True, True, 0)
        root.pack_start(sbar_box, False, False, 0)

        self._build_sidebar()
        self.main_stack.set_visible_child_name("empty")

        # Poll running status every 3s
        GLib.timeout_add_seconds(3, self._poll_status)

        self.show_all()

    # -- Header ---------------------------------------------------------------

    def _build_header(self):
        hdr = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        add_class(hdr, "header")

        # el puto logo
        left = Gtk.Box(spacing=8)
        left.set_margin_start(12)
        _banner_path = "/usr/local/essora-vm/essora-vm.png"
        _banner_shown = False
        if os.path.isfile(_banner_path):
            try:
                from gi.repository import GdkPixbuf
                pb_orig = GdkPixbuf.Pixbuf.new_from_file(_banner_path)
                orig_w, orig_h = pb_orig.get_width(), pb_orig.get_height()
                target_h = 44
                target_w = int(orig_w * target_h / orig_h)
                if target_w > 220:
                    target_w = 220
                    target_h = int(orig_h * target_w / orig_w)
                pb = pb_orig.scale_simple(target_w, target_h, GdkPixbuf.InterpType.BILINEAR)
                banner_img = Gtk.Image.new_from_pixbuf(pb)
                banner_img.set_valign(Gtk.Align.CENTER)
                left.pack_start(banner_img, False, False, 0)
                _banner_shown = True
            except Exception:
                pass
        if not _banner_shown:
            _logo_path = "/usr/local/essora-vm/logo-essora-vm.png"
            if os.path.isfile(_logo_path):
                try:
                    from gi.repository import GdkPixbuf
                    pb2 = GdkPixbuf.Pixbuf.new_from_file_at_scale(_logo_path, 36, 36, True)
                    left.pack_start(Gtk.Image.new_from_pixbuf(pb2), False, False, 0)
                except Exception:
                    pass
            lbl_essora = Gtk.Label()
            lbl_essora.set_markup('<span size="13000" weight="bold" foreground="#ffffff">Essora</span>')
            left.pack_start(lbl_essora, False, False, 4)

        hdr.pack_start(left, True, True, 0)

        # "Essora VM" centrado de titulo
        center = Gtk.Box()
        center.set_halign(Gtk.Align.CENTER)
        self._hdr_title = Gtk.Label()
        self._hdr_title.set_markup(
            '<span size="13000" weight="bold" foreground="#ffffff">Essora VM</span>'
        )
        center.pack_start(self._hdr_title, False, False, 0)
        hdr.set_center_widget(center)

        right = Gtk.Box(spacing=6)
        right.set_margin_end(12)
        right.set_halign(Gtk.Align.END)

        self.btn_new = Gtk.Button(label=self.tr["new_vm"])
        add_class(self.btn_new, "btn-new-vm")
        self.btn_new.connect("clicked", self._on_new_vm)

        self.btn_settings = Gtk.Button(label=self.tr["settings"])
        add_class(self.btn_settings, "btn-header")
        self.btn_settings.connect("clicked", self._on_settings)

        self.btn_close = Gtk.Button(label=self.tr["close"])
        add_class(self.btn_close, "btn-header")
        self.btn_close.connect("clicked", lambda _: self._on_close())

        right.pack_start(self.btn_new, False, False, 0)
        right.pack_start(self.btn_settings, False, False, 0)
        right.pack_start(self.btn_close, False, False, 0)
        hdr.pack_end(right, False, False, 0)

        return hdr

    def _show_app_menu(self, btn):
        tr = self.tr
        menu = Gtk.Menu()

        # Settings
        item_cfg = Gtk.MenuItem(label=tr["settings"])
        item_cfg.connect("activate", self._on_settings)
        menu.append(item_cfg)

        menu.append(Gtk.SeparatorMenuItem())

        # Minimize
        item_min = Gtk.MenuItem(label=tr.get("minimize", "Minimize"))
        item_min.connect("activate", lambda _: self.iconify())
        menu.append(item_min)

        # Maximize / Restore
        item_max = Gtk.MenuItem(label=tr.get("maximize", "Maximize"))
        def _toggle_max(_):
            if self.get_window() and self.get_window().get_state() & Gdk.WindowState.MAXIMIZED:
                self.unmaximize()
            else:
                self.maximize()
        item_max.connect("activate", _toggle_max)
        menu.append(item_max)

        menu.append(Gtk.SeparatorMenuItem())

        # About
        item_about = Gtk.MenuItem(label=tr.get("about", "About"))
        item_about.connect("activate", self._on_about)
        menu.append(item_about)

        menu.append(Gtk.SeparatorMenuItem())

        # Close
        item_close = Gtk.MenuItem(label=tr["close"])
        item_close.connect("activate", lambda _: self._on_close())
        menu.append(item_close)

        menu.show_all()
        menu.popup_at_widget(btn, Gdk.Gravity.SOUTH_EAST, Gdk.Gravity.NORTH_EAST, None)

    def _on_about(self, _=None):
        tr = self.tr
        dlg = Gtk.Dialog(title=tr.get("about_title", "About Essora VM"), parent=self,
                         flags=Gtk.DialogFlags.MODAL)
        dlg.set_default_size(400, 340)
        dlg.set_resizable(False)
        ca = dlg.get_content_area()
        ca.set_spacing(0)

        # Top section with logo + app name + version
        top = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        top.set_margin_top(24); top.set_margin_bottom(14)

        # Logo
        _logo = "/usr/local/essora-vm/logo-essora-vm.png"
        if os.path.isfile(_logo):
            try:
                from gi.repository import GdkPixbuf
                pb = GdkPixbuf.Pixbuf.new_from_file_at_scale(_logo, 90, 90, True)
                img = Gtk.Image.new_from_pixbuf(pb)
                img.set_halign(Gtk.Align.CENTER)
                top.pack_start(img, False, False, 0)
            except Exception:
                pass
        else:
            ico = Gtk.Label(); ico.set_markup('<span size="48000">🌿</span>')
            ico.set_halign(Gtk.Align.CENTER); top.pack_start(ico, False, False, 0)

        # App name — big
        app_lbl = Gtk.Label(); app_lbl.set_halign(Gtk.Align.CENTER)
        app_lbl.set_markup('<span size="20000" weight="bold" foreground="#4ade80">Essora VM</span>')
        top.pack_start(app_lbl, False, False, 0)

        # Version subtitle
        ver_lbl = Gtk.Label(); ver_lbl.set_halign(Gtk.Align.CENTER)
        ver_lbl.set_markup('<span size="12000" foreground="#a6adc8">Version 1.3</span>')
        top.pack_start(ver_lbl, False, False, 0)

        ca.pack_start(top, False, False, 0)

        # Separator
        ca.pack_start(Gtk.Separator(), False, False, 4)

        # Info grid — bigger font via markup
        grid = Gtk.Grid()
        grid.set_column_spacing(20); grid.set_row_spacing(12)
        grid.set_margin_start(40); grid.set_margin_end(40)
        grid.set_margin_top(12); grid.set_margin_bottom(20)
        grid.set_halign(Gtk.Align.CENTER)

        def _row(grid, r, key, val):
            k = Gtk.Label(); k.set_halign(Gtk.Align.END)
            k.set_markup(f'<span size="11500" foreground="#9ca3af">{key}:</span>')
            v = Gtk.Label(); v.set_halign(Gtk.Align.START)
            v.set_markup(f'<span size="11500" weight="bold" foreground="#f3f4f6">{val}</span>')
            grid.attach(k, 0, r, 1, 1); grid.attach(v, 1, r, 1, 1)

        _row(grid, 0, tr.get("about_version", "Version"),  "1.3")
        _row(grid, 1, tr.get("about_author",  "Author"),   "josejp2424")
        _row(grid, 2, tr.get("about_dev",     "Role"),     "Essora Developer")
        _row(grid, 3, tr.get("about_license", "License"),  "GPL-3.0")
        _row(grid, 4, "Distro",                             "Essora Linux")
        ca.pack_start(grid, False, False, 0)

        btn_ok = dlg.add_button("OK", Gtk.ResponseType.OK)
        add_class(btn_ok, "btn-new-vm")
        dlg.show_all()
        dlg.run()
        dlg.destroy()

    #  Language bar 

    def _build_lang_bar(self):
        bar = Gtk.Box(spacing=8)
        add_class(bar, "lang-bar")
        bar.set_margin_start(16); bar.set_margin_end(16)
        bar.set_margin_top(3); bar.set_margin_bottom(3)
        bar.pack_start(Gtk.Label(), True, True, 0)
        lbl = Gtk.Label(label=self.tr["language"] + ":")
        bar.pack_start(lbl, False, False, 0)
        self.lang_combo = Gtk.ComboBoxText()
        for code, name in LANGUAGE_NAMES.items():
            self.lang_combo.append(code, name)
        self.lang_combo.set_active_id(self.lang)
        self.lang_combo.connect("changed", self._on_lang_changed)
        bar.pack_start(self.lang_combo, False, False, 0)
        return bar


    def _build_sidebar(self):
        for child in self.sidebar_box.get_children():
            self.sidebar_box.remove(child)

        title = Gtk.Label(label=self.tr["my_vms"])
        title.set_halign(Gtk.Align.START)
        add_class(title, "sidebar-title")
        self.sidebar_box.pack_start(title, False, False, 0)

        self.vm_buttons = []
        self.vm_dot_labels = [] 
        for i, vm in enumerate(self.vms):
            running = is_running(vm["name"], self.pids)
            btn, dot = self._make_vm_row(vm, running, i)
            self.sidebar_box.pack_start(btn, False, False, 0)
            self.vm_buttons.append(btn)
            self.vm_dot_labels.append(dot)

        self.sidebar_box.show_all()

    def _make_vm_row(self, vm, running, idx):
        btn = Gtk.Button()
        btn.set_relief(Gtk.ReliefStyle.NONE)
        add_class(btn, "vm-row")
        hbox = Gtk.Box(spacing=8)
        dot = Gtk.Label()
        dot.set_markup(
            '<span color="#22c55e">●</span>' if running
            else '<span color="#4b5563">●</span>'
        )
        name_lbl = Gtk.Label(label=vm["name"])
        name_lbl.set_halign(Gtk.Align.START)
        hbox.pack_start(dot, False, False, 0)
        hbox.pack_start(name_lbl, True, True, 0)
        btn.add(hbox)
        btn.connect("clicked", self._on_select_vm, idx)
        return btn, dot


    def _build_empty_page(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box.set_halign(Gtk.Align.CENTER); box.set_valign(Gtk.Align.CENTER)
        icon = Gtk.Label(); icon.set_markup('<span size="48000">🖥️</span>')
        t = Gtk.Label(label=self.tr["no_vm"]); add_class(t, "empty-title")
        s = Gtk.Label(label=self.tr["no_vm_sub"]); add_class(s, "empty-sub")
        s.set_justify(Gtk.Justification.CENTER)
        box.pack_start(icon, False, False, 0)
        box.pack_start(t, False, False, 0)
        box.pack_start(s, False, False, 0)
        box.show_all()
        return box


    def _build_detail_page(self, vm):
        """Build the right-panel detail view for a given VM dict."""
        running = is_running(vm["name"], self.pids)
        tr = self.tr

        outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        add_class(outer, "content-area")
        outer.set_hexpand(True); outer.set_vexpand(True)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_hexpand(True); scroll.set_vexpand(True)
        inner = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        inner.set_margin_start(4); inner.set_margin_end(4)
        scroll.add(inner)
        outer.pack_start(scroll, True, True, 0)

        # VM Name title
        name_lbl = Gtk.Label(label=vm["name"])
        name_lbl.set_halign(Gtk.Align.START)
        add_class(name_lbl, "vm-name-title")
        inner.pack_start(name_lbl, False, False, 0)

        # Top row: preview + info
        top_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        inner.pack_start(top_row, False, False, 0)

        # Preview box
        preview = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        add_class(preview, "preview-box")
        preview.set_size_request(480, 280)
        preview.set_halign(Gtk.Align.START)

        # Gtk.Image — shows screendump when running, placeholder when stopped
        self._preview_img = Gtk.Image()
        self._preview_img.set_vexpand(True)
        self._preview_img.set_valign(Gtk.Align.CENTER)
        self._preview_img.set_halign(Gtk.Align.CENTER)
        self._set_preview_placeholder(vm["name"])
        ph_text = Gtk.Label(label=vm["name"])
        add_class(ph_text, "preview-placeholder-text")
        ph_text.set_halign(Gtk.Align.CENTER)
        ph_text.set_margin_bottom(12)
        preview.pack_start(self._preview_img, True, True, 0)
        preview.pack_start(ph_text, False, False, 0)
        top_row.pack_start(preview, False, False, 0)

        # Info panel
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        info_box.set_valign(Gtk.Align.CENTER)
        info_box.set_margin_start(8)

        ram_gb = vm.get("ram", 1024) / 1024
        ram_str = f"{ram_gb:.0f} GB" if ram_gb == int(ram_gb) else f"{vm.get('ram',1024)} MB"
        disk_gb = vm.get("disk_size", 20)

        status_str = tr["vm_running"] if running else tr["vm_stopped"]
        status_color = "#22c55e" if running else "#9ca3af"

        for label_key, value in [
            (tr["cpu_label"],  f'{vm.get("cpu", 2)} {tr["cores"]}'),
            (tr["ram_label"],  ram_str),
            (tr["disk_label"], f'{disk_gb} GB (qcow2)'),
        ]:
            row = Gtk.Box(spacing=8)
            k = Gtk.Label(label=label_key); add_class(k, "info-label")
            k.set_width_chars(8); k.set_halign(Gtk.Align.START)
            v = Gtk.Label(label=value); add_class(v, "info-value")
            v.set_halign(Gtk.Align.START)
            row.pack_start(k, False, False, 0)
            row.pack_start(v, False, False, 0)
            info_box.pack_start(row, False, False, 0)

        # Status
        st_row = Gtk.Box(spacing=8)
        st_lbl = Gtk.Label(label="Status:"); add_class(st_lbl, "info-label")
        st_lbl.set_width_chars(8); st_lbl.set_halign(Gtk.Align.START)
        st_val = Gtk.Label()
        st_val.set_markup(f'<span color="{status_color}" weight="bold">{status_str}</span>')
        st_val.set_halign(Gtk.Align.START)
        self._status_val_label = st_val 
        st_row.pack_start(st_lbl, False, False, 0)
        st_row.pack_start(st_val, False, False, 0)
        info_box.pack_start(st_row, False, False, 0)

        top_row.pack_start(info_box, True, True, 0)

        btn_row = Gtk.Box(spacing=8)
        btn_row.set_margin_top(4)

        self._btn_start   = Gtk.Button(label=tr["start"])
        self._btn_stop    = Gtk.Button(label=tr["stop"])
        self._btn_restart = Gtk.Button(label=tr["restart"])
        self._btn_delete  = Gtk.Button(label=tr["delete"])

        add_class(self._btn_start,   "btn-start")
        add_class(self._btn_stop,    "btn-stop")
        add_class(self._btn_restart, "btn-restart")
        add_class(self._btn_delete,  "btn-delete")

        self._btn_start.connect("clicked",   self._on_start)
        self._btn_stop.connect("clicked",    self._on_stop)
        self._btn_restart.connect("clicked", self._on_restart)
        self._btn_delete.connect("clicked",  self._on_delete)

        for b in [self._btn_start, self._btn_stop, self._btn_restart, self._btn_delete]:
            btn_row.pack_start(b, False, False, 0)

        inner.pack_start(btn_row, False, False, 0)

        cfg = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        add_class(cfg, "config-area")
        inner.pack_start(cfg, False, False, 0)

        # ISO / CD-ROM
        iso_row = Gtk.Box(spacing=10)
        iso_lbl = Gtk.Label(label=tr["iso_label"])
        add_class(iso_lbl, "config-label")
        iso_lbl.set_halign(Gtk.Align.START)
        self._iso_entry = Gtk.Entry()
        self._iso_entry.set_text(vm.get("iso", ""))
        self._iso_entry.set_hexpand(True)
        self._iso_entry.set_placeholder_text(".iso path (optional)")
        btn_biso = Gtk.Button(label=tr["browse"])
        btn_biso.connect("clicked", self._browse_iso)
        iso_row.pack_start(iso_lbl, False, False, 0)
        iso_row.pack_start(self._iso_entry, True, True, 0)
        iso_row.pack_start(btn_biso, False, False, 0)
        cfg.pack_start(iso_row, False, False, 0)

        # CPU slider
        cpu_row = Gtk.Box(spacing=10)
        cpu_lbl = Gtk.Label(label=tr["cpu_cfg"])
        add_class(cpu_lbl, "config-label")
        cpu_lbl.set_halign(Gtk.Align.START)
        cur_cpu = vm.get("cpu", 2)
        self._cpu_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 1, 16, 1)
        self._cpu_scale.set_value(cur_cpu)
        self._cpu_scale.set_digits(0)
        self._cpu_scale.set_draw_value(True)
        self._cpu_scale.set_hexpand(True)
        self._cpu_scale.set_size_request(160, -1)
        self._cpu_val_lbl = Gtk.Label(label=str(cur_cpu))
        add_class(self._cpu_val_lbl, "info-value")
        self._cpu_val_lbl.set_width_chars(3)
        self._cpu_scale.connect("value-changed", self._on_cpu_changed)
        cpu_row.pack_start(cpu_lbl, False, False, 0)
        cpu_row.pack_start(self._cpu_scale, True, True, 0)
        cfg.pack_start(cpu_row, False, False, 0)

        # RAM slider
        ram_row = Gtk.Box(spacing=10)
        ram_lbl = Gtk.Label(label=tr["ram_cfg"])
        add_class(ram_lbl, "config-label")
        ram_lbl.set_halign(Gtk.Align.START)
        cur_ram = vm.get("ram", 2048)
        _ram_steps = [512, 1024, 2048, 4096, 6144, 8192]
        _ram_idx = _ram_steps.index(cur_ram) if cur_ram in _ram_steps else 2
        self._ram_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 5, 1)
        self._ram_scale.set_value(_ram_idx)
        self._ram_scale.set_digits(0)
        self._ram_scale.set_draw_value(False)
        self._ram_scale.set_hexpand(True)
        self._ram_scale.set_size_request(160, -1)

        for i, v in enumerate(_ram_steps):
            self._ram_scale.add_mark(i, Gtk.PositionType.BOTTOM, None)
        self._ram_val_lbl = Gtk.Label()
        add_class(self._ram_val_lbl, "info-value")
        self._ram_val_lbl.set_width_chars(7)
        self._ram_val_lbl.set_markup(self._ram_mb_to_str(cur_ram))
        self._ram_scale.connect("value-changed", self._on_ram_changed)
        ram_row.pack_start(ram_lbl, False, False, 0)
        ram_row.pack_start(self._ram_scale, True, True, 0)
        ram_row.pack_start(self._ram_val_lbl, False, False, 0)
        cfg.pack_start(ram_row, False, False, 0)

        bottom_row = Gtk.Box(spacing=16)
        self._kvm_check = Gtk.CheckButton(label=tr.get("enable_kvm", "Enable KVM"))
        self._kvm_check.set_tooltip_text(tr.get("kvm_tooltip", "Uses kernel driver for near-native performance."))

        _kvm_arch = vm.get("arch", "x86_64")
        _kvm_non_x86 = ("riscv" in _kvm_arch or "arm" in _kvm_arch or "aarch" in _kvm_arch or "mips" in _kvm_arch or "ppc" in _kvm_arch or "s390" in _kvm_arch or "sparc" in _kvm_arch)
        if _kvm_non_x86:
            self._kvm_check.set_active(False)
            self._kvm_check.set_sensitive(False)
            self._kvm_check.set_tooltip_text("KVM not available for non-x86 guests on x86 host.")
        elif not os.path.exists("/dev/kvm"):
            self._kvm_check.set_active(False)
            self._kvm_check.set_sensitive(False)
            self._kvm_check.set_tooltip_text("/dev/kvm not available on this system.")
        else:
            self._kvm_check.set_active(vm.get("kvm", True))
        btn_save_cfg = Gtk.Button(label=tr["save"])
        add_class(btn_save_cfg, "btn-restart")
        btn_save_cfg.connect("clicked", self._on_save_cfg)
        bottom_row.pack_start(self._kvm_check, False, False, 0)
        bottom_row.pack_start(Gtk.Label(), True, True, 0)
        bottom_row.pack_start(btn_save_cfg, False, False, 0)
        cfg.pack_start(bottom_row, False, False, 0)

        # Non-x86 fields: only shown for riscv64, arm, aarch64, etc.
        _arch = vm.get("arch", "x86_64")
        _needs_extra = ("riscv" in _arch or "arm" in _arch or "aarch" in _arch or "mips" in _arch or "ppc" in _arch or "s390" in _arch or "sparc" in _arch)
        if _needs_extra:
            cfg.pack_start(Gtk.Separator(), False, False, 4)

            tip = Gtk.Label(label="RISC-V / ARM — required fields")
            add_class(tip, "config-label")
            tip.set_halign(Gtk.Align.START)
            tip.set_markup('<span foreground="#4ade80" size="9500">RISC-V / ARM — required fields</span>')
            cfg.pack_start(tip, False, False, 0)

            # Machine type
            mach_row = Gtk.Box(spacing=10)
            mach_lbl = Gtk.Label(label="Machine:")
            add_class(mach_lbl, "config-label")
            mach_lbl.set_halign(Gtk.Align.START); mach_lbl.set_width_chars(16)
            self._machine_entry = Gtk.Entry()
            self._machine_entry.set_text(vm.get("machine", "virt"))
            self._machine_entry.set_hexpand(True)
            self._machine_entry.set_placeholder_text("virt  /  sifive_u  /  raspi3b")
            mach_row.pack_start(mach_lbl, False, False, 0)
            mach_row.pack_start(self._machine_entry, True, True, 0)
            cfg.pack_start(mach_row, False, False, 0)

            # Firmware / BIOS (OpenSBI for RISC-V)
            bios_row = Gtk.Box(spacing=10)
            bios_lbl = Gtk.Label(label="Firmware / BIOS:")
            add_class(bios_lbl, "config-label")
            bios_lbl.set_halign(Gtk.Align.START); bios_lbl.set_width_chars(16)
            self._bios_entry = Gtk.Entry()
            _bios_default = {
                "riscv64": "/usr/lib/riscv64-linux-gnu/opensbi/generic/fw_dynamic.bin",
                "aarch64": "/usr/share/qemu-efi-aarch64/QEMU_EFI.fd",
            }
            _bios_val = vm.get("bios") or _bios_default.get(_arch, "")
            self._bios_entry.set_text(_bios_val)
            self._bios_entry.set_hexpand(True)
            self._bios_entry.set_placeholder_text(
                "/usr/lib/riscv64-linux-gnu/opensbi/generic/fw_dynamic.bin")
            btn_bios = Gtk.Button(label=tr["browse"])
            btn_bios.connect("clicked", self._browse_bios)
            bios_row.pack_start(bios_lbl, False, False, 0)
            bios_row.pack_start(self._bios_entry, True, True, 0)
            bios_row.pack_start(btn_bios, False, False, 0)
            cfg.pack_start(bios_row, False, False, 0)

            # Kernel image (U-Boot or Linux kernel)
            kern_row = Gtk.Box(spacing=10)
            kern_lbl = Gtk.Label(label="Kernel / U-Boot:")
            add_class(kern_lbl, "config-label")
            kern_lbl.set_halign(Gtk.Align.START); kern_lbl.set_width_chars(16)
            self._kernel_entry = Gtk.Entry()
            _kernel_default = {
                "riscv64": "/usr/lib/u-boot/qemu-riscv64_smode/uboot.elf",
            }
            _kern_val = vm.get("kernel") or _kernel_default.get(_arch, "")
            self._kernel_entry.set_text(_kern_val)
            self._kernel_entry.set_hexpand(True)
            self._kernel_entry.set_placeholder_text("u-boot.bin  /  Image  /  vmlinuz")
            btn_kern = Gtk.Button(label=tr["browse"])
            btn_kern.connect("clicked", self._browse_kernel)
            kern_row.pack_start(kern_lbl, False, False, 0)
            kern_row.pack_start(self._kernel_entry, True, True, 0)
            kern_row.pack_start(btn_kern, False, False, 0)
            cfg.pack_start(kern_row, False, False, 0)

            # Extra QEMU args
            extra_row = Gtk.Box(spacing=10)
            extra_lbl = Gtk.Label(label="Extra args:")
            add_class(extra_lbl, "config-label")
            extra_lbl.set_halign(Gtk.Align.START); extra_lbl.set_width_chars(16)
            self._extra_entry = Gtk.Entry()
            _extra_default = {
                "riscv64": "",
                "aarch64": "",
                "arm":     "",
            }
            _extra_val = vm.get("extra_args") or _extra_default.get(_arch, "")
            self._extra_entry.set_text(_extra_val)
            self._extra_entry.set_hexpand(True)
            self._extra_entry.set_placeholder_text("-nographic  /  -serial mon:stdio")
            extra_row.pack_start(extra_lbl, False, False, 0)
            extra_row.pack_start(self._extra_entry, True, True, 0)
            cfg.pack_start(extra_row, False, False, 0)

        else:  # x86/amd64 — no extra fields needed
            self._machine_entry = None
            self._bios_entry    = None
            self._kernel_entry  = None
            self._extra_entry   = None

        outer.show_all()
        return outer

    def _ram_mb_to_str(self, mb):
        _ram_steps = [512, 1024, 2048, 4096, 6144, 8192]
        idx = max(0, min(int(mb), 5))
        real_mb = _ram_steps[idx]
        if real_mb >= 1024:
            return f'<b>{real_mb // 1024} GB</b>'
        return f'<b>{real_mb} MB</b>'

    def _on_cpu_changed(self, scale):
        v = int(scale.get_value())
        if hasattr(self, "_cpu_val_lbl"):
            self._cpu_val_lbl.set_text(str(v))

    def _on_ram_changed(self, scale):
        _ram_steps = [512, 1024, 2048, 4096, 6144, 8192]
        idx = max(0, min(int(scale.get_value()), 5))
        if hasattr(self, "_ram_val_lbl"):
            self._ram_val_lbl.set_markup(self._ram_mb_to_str(idx))

    def _set_preview_placeholder(self, name=""):
        """Show a computer icon placeholder in the preview widget."""
        if not hasattr(self, "_preview_img"):
            return

        self._preview_img.set_from_icon_name("computer", Gtk.IconSize.DIALOG)

    def _update_preview(self):
        """Called by timer: grab screendump from QEMU monitor and show it."""
        vm = self.selected_vm
        if vm is None or not hasattr(self, "_preview_img"):
            return False
        if not is_running(vm.get("name",""), self.pids):
            self._set_preview_placeholder(vm.get("name",""))
            return False  

        sock_path = os.path.join(CONFIG_DIR, vm["name"] + ".monitor")
        dump_path = os.path.join(CONFIG_DIR, vm["name"] + ".ppm")
        if not os.path.exists(sock_path):
            return True  

        try:
            import socket as _sock
            s = _sock.socket(_sock.AF_UNIX, _sock.SOCK_STREAM)
            s.settimeout(1)
            s.connect(sock_path)
            s.recv(1024)  
            s.sendall(f"screendump {dump_path}\n".encode())
            s.recv(256)
            s.close()
        except Exception:
            return True  

        if os.path.isfile(dump_path):
            try:
                from gi.repository import GdkPixbuf
                pb = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    dump_path, 478, 270, False
                )
                self._preview_img.set_from_pixbuf(pb)
            except Exception:
                pass

        return True 

    def _set_status(self, msg):
        self.statusbar.set_text(msg)
        GLib.timeout_add_seconds(6, lambda: self.statusbar.set_text("Essora VM  •  QEMU Frontend") or False)

    def _show_info(self, msg, error=False):
        mtype = Gtk.MessageType.ERROR if error else Gtk.MessageType.INFO
        d = Gtk.MessageDialog(parent=self, message_type=mtype,
                               buttons=Gtk.ButtonsType.OK, text=msg)
        d.run(); d.destroy()

    def _refresh_sidebar(self):
        """Update sidebar dot colors in-place — never rebuild the widget tree."""
        dots = getattr(self, "vm_dot_labels", [])
        for i, (vm, dot) in enumerate(zip(self.vms, dots)):
            running = is_running(vm["name"], self.pids)
            dot.set_markup(
                '<span color="#22c55e">●</span>' if running
                else '<span color="#4b5563">●</span>'
            )

    def _refresh_detail(self):
        if self.selected_vm is None:
            return
        new_page = self._build_detail_page(self.selected_vm)
        old = self.main_stack.get_child_by_name("detail")
        if old:
            self.main_stack.remove(old)
        self.detail_page = new_page
        self.main_stack.add_named(self.detail_page, "detail")
        self.main_stack.set_visible_child_name("detail")


    def _on_select_vm(self, _btn, idx):
        self.selected_idx = idx
        self.selected_vm  = self.vms[idx]
        for i, b in enumerate(self.vm_buttons):
            ctx = b.get_style_context()
            if i == idx:
                ctx.add_class("vm-row-selected")
            else:
                ctx.remove_class("vm-row-selected")
        self._refresh_detail()

    def _on_new_vm(self, _):
        existing = {vm["name"] for vm in self.vms}
        dlg = NewVMDialog(self, self.tr, existing)
        while True:
            resp = dlg.run()
            if resp == Gtk.ResponseType.OK:
                vm = dlg.get_vm()
                if vm:
                    self.vms.append(vm)
                    save_vms(self.vms)
                    self._build_sidebar()
                    self.selected_idx = len(self.vms) - 1
                    self.selected_vm  = self.vms[-1]
                    self._refresh_detail()
                    break
            else:
                break
        dlg.destroy()

    def _on_settings(self, _):
        dlg = SettingsDialog(self, self.tr, self.settings)
        if dlg.run() == Gtk.ResponseType.OK:
            self.settings["qemu_bin"] = dlg.get_qemu_bin()
            save_settings(self.settings)
            self._set_status(self.tr["saved"])
        dlg.destroy()

    def _on_lang_changed(self, combo):
        code = combo.get_active_id()
        if code and code in TRANSLATIONS and code != self.lang:
            self.lang = code
            self.tr = TRANSLATIONS[code]
            self.settings["lang"] = code
            save_settings(self.settings)
            self._rebuild_ui()

    def _rebuild_ui(self):
        """Rebuild translatable header buttons + sidebar + detail."""
        self.btn_new.set_label(self.tr["new_vm"])
        self.btn_settings.set_label(self.tr["settings"])
        self.btn_close.set_label(self.tr["close"])
        if hasattr(self, "_about_lbl"):
            self._about_lbl.set_markup(
                f'<span foreground="#4ade80" underline="single">{self.tr.get("about","About")}</span>')
        self._build_sidebar()
        if self.selected_vm:
            self._refresh_detail()
        else:
            old = self.main_stack.get_child_by_name("empty")
            if old:
                self.main_stack.remove(old)
            self.empty_page = self._build_empty_page()
            self.main_stack.add_named(self.empty_page, "empty")
            self.main_stack.set_visible_child_name("empty")

    def _on_start(self, _):
        vm = self.selected_vm
        if vm is None:
            return

        arch = vm.get("arch", "x86_64")
        qemu_bin = f"qemu-system-{arch}"

        iso   = self._iso_entry.get_text().strip() if hasattr(self, "_iso_entry") else vm.get("iso", "")
        disk  = vm.get("disk", "")
        _ram_steps = [512, 1024, 2048, 4096, 6144, 8192]
        try:
            cpu = int(self._cpu_scale.get_value())
        except Exception:
            cpu = vm.get("cpu", 2)
        try:
            ram = _ram_steps[max(0, min(int(self._ram_scale.get_value()), 5))]
        except Exception:
            ram = vm.get("ram", 2048)
        use_kvm = self._kvm_check.get_active() if hasattr(self, "_kvm_check") else vm.get("kvm", True)

        boot = "d" if (not disk or not os.path.isfile(disk)) else "c"
        if iso and os.path.isfile(iso):
            boot = "d"  

        sock_path = os.path.join(CONFIG_DIR, vm["name"] + ".monitor")

        try:
            os.remove(sock_path)
        except Exception:
            pass

        _needs_extra = ("riscv" in arch or "arm" in arch or "aarch" in arch or "mips" in arch or "ppc" in arch or "s390" in arch or "sparc" in arch)

        cmd = [qemu_bin]
        cmd += ["-m", str(ram)]
        cmd += ["-smp", str(cpu)]
        cmd += ["-monitor", f"unix:{sock_path},server,nowait"]

        if _needs_extra:
            # RISC-V / ARM: machine, firmware, kernel
            machine = vm.get("machine", "virt")
            if machine:
                cmd += ["-machine", machine]
            bios = vm.get("bios", "")
            if bios and os.path.isfile(bios):
                cmd += ["-bios", bios]
            kernel = vm.get("kernel", "")
            if kernel and os.path.isfile(kernel):
                cmd += ["-kernel", kernel]
            if disk and os.path.isfile(disk):
                cmd += ["-drive", f"file={disk},format=qcow2,if=none,id=hd0",
                        "-device", "virtio-blk-device,drive=hd0"]
            if iso and os.path.isfile(iso):
                cmd += ["-drive", f"file={iso},format=raw,if=none,readonly=on,id=cd0",
                        "-device", "virtio-blk-device,drive=cd0"]
            cmd += ["-netdev", "user,id=net0",
                    "-device", "virtio-net-device,netdev=net0"]

            extra = vm.get("extra_args", "")
            if extra.strip():
                cmd += shlex.split(extra)
        else:  
            cmd += ["-boot", boot]
            if use_kvm and os.path.exists("/dev/kvm"):
                cmd.append("-enable-kvm")
            if disk and os.path.isfile(disk):
                cmd += ["-hda", disk]
            if iso and os.path.isfile(iso):
                try:
                    mounts = open("/proc/mounts").read()
                    if iso in mounts:
                        subprocess.run(["umount", iso], capture_output=True)
                except Exception:
                    pass
                cmd += ["-drive", f"file={iso},media=cdrom,readonly=on,format=raw"]

        env = os.environ.copy()
        env["QEMU_SOUND_DRV"] = "alsa"

        try:
            proc = subprocess.Popen(cmd, env=env)
            self.pids[vm["name"]] = proc.pid
            save_pids(self.pids)
            self._set_status(self.tr["started_ok"])
            GLib.timeout_add(1500, self._refresh_after_action)
            GLib.timeout_add(3000, self._update_preview)
        except FileNotFoundError:
            self._show_info(f"QEMU binary not found: {qemu_bin}", error=True)
        except Exception as e:
            self._show_info(str(e), error=True)

    def _on_stop(self, _):
        vm = self.selected_vm
        if vm is None:
            return
        if hasattr(self, "_preview_img"):
            self._set_preview_placeholder(vm.get("name", ""))
        pid = self.pids.get(vm["name"])
        if pid:
            try:
                os.kill(int(pid), signal.SIGTERM)
            except Exception:
                pass
            self.pids.pop(vm["name"], None)
            save_pids(self.pids)
        self._set_status(self.tr["stopped_ok"])
        GLib.timeout_add(800, self._refresh_after_action)

    def _on_restart(self, _):
        self._on_stop(None)
        GLib.timeout_add(1200, lambda: self._on_start(None) or False)
        self._set_status(self.tr["restarted_ok"])

    def _on_delete(self, _):
        vm = self.selected_vm
        if vm is None:
            return
        tr = self.tr
        d = Gtk.MessageDialog(parent=self, message_type=Gtk.MessageType.QUESTION,
                               buttons=Gtk.ButtonsType.NONE,
                               text=f'{tr["confirm_del2"]} "{vm["name"]}"?')
        d.set_title(tr["confirm_del"])
        d.add_button(tr["cancel"],    Gtk.ResponseType.CANCEL)
        d.add_button(tr["delete_btn"], Gtk.ResponseType.OK)
        if d.run() == Gtk.ResponseType.OK:
            self._on_stop(None)
            self.vms.remove(vm)
            save_vms(self.vms)
            self.selected_vm  = None
            self.selected_idx = -1
            self._build_sidebar()
            self.main_stack.set_visible_child_name("empty")
        d.destroy()

    def _on_save_cfg(self, _):
        """Save current config panel values back into the VM dict."""
        vm = self.selected_vm
        if vm is None:
            return
        vm["iso"] = self._iso_entry.get_text().strip() if hasattr(self, "_iso_entry") else vm.get("iso", "")
        try:
            _ram_steps = [512, 1024, 2048, 4096, 6144, 8192]
            vm["cpu"] = int(self._cpu_scale.get_value())
            vm["ram"] = _ram_steps[max(0, min(int(self._ram_scale.get_value()), 5))]
        except Exception:
            pass
        vm["kvm"] = self._kvm_check.get_active() if hasattr(self, "_kvm_check") else True
        if hasattr(self, "_machine_entry") and self._machine_entry:
            vm["machine"]    = self._machine_entry.get_text().strip()
        if hasattr(self, "_bios_entry") and self._bios_entry:
            vm["bios"]       = self._bios_entry.get_text().strip()
        if hasattr(self, "_kernel_entry") and self._kernel_entry:
            vm["kernel"]     = self._kernel_entry.get_text().strip()
        if hasattr(self, "_extra_entry") and self._extra_entry:
            vm["extra_args"] = self._extra_entry.get_text().strip()
        save_vms(self.vms)
        self._set_status(self.tr["saved"])

    def _browse_bios(self, _):
        d = Gtk.FileChooserDialog(title="Firmware / BIOS", parent=self,
                                   action=Gtk.FileChooserAction.OPEN)
        d.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        d.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        if d.run() == Gtk.ResponseType.OK:
            if hasattr(self, "_bios_entry") and self._bios_entry:
                self._bios_entry.set_text(d.get_filename())
        d.destroy()

    def _browse_kernel(self, _):
        d = Gtk.FileChooserDialog(title="Kernel / U-Boot Image", parent=self,
                                   action=Gtk.FileChooserAction.OPEN)
        d.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        d.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        if d.run() == Gtk.ResponseType.OK:
            if hasattr(self, "_kernel_entry") and self._kernel_entry:
                self._kernel_entry.set_text(d.get_filename())
        d.destroy()

    def _browse_iso(self, _):
        d = Gtk.FileChooserDialog(title=self.tr["iso_label"], parent=self,
                                   action=Gtk.FileChooserAction.OPEN)
        d.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        d.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        f = Gtk.FileFilter(); f.add_pattern("*.iso"); f.set_name("ISO files")
        d.add_filter(f)
        if d.run() == Gtk.ResponseType.OK:
            self._iso_entry.set_text(d.get_filename())
        d.destroy()

    def _poll_status(self):
        """Update dots and status label in-place — zero widget reconstruction."""
        self._refresh_sidebar()
        if self.selected_vm and hasattr(self, "_status_val_label"):
            running = is_running(self.selected_vm["name"], self.pids)
            tr = self.tr
            status_str = tr["vm_running"] if running else tr["vm_stopped"]
            color = "#22c55e" if running else "#9ca3af"
            self._status_val_label.set_markup(
                f'<span color="{color}" weight="bold">{status_str}</span>'
            )
        return True  

    def _refresh_after_action(self):
        """Called after start/stop — only update in-place, never rebuild."""
        self._refresh_sidebar()
        if self.selected_vm and hasattr(self, "_status_val_label"):
            running = is_running(self.selected_vm["name"], self.pids)
            tr = self.tr
            status_str = tr["vm_running"] if running else tr["vm_stopped"]
            color = "#22c55e" if running else "#9ca3af"
            self._status_val_label.set_markup(
                f'<span color="{color}" weight="bold">{status_str}</span>'
            )
        return False

    def _on_close(self, *_):
        save_settings(self.settings)
        save_vms(self.vms)
        save_pids(self.pids)
        Gtk.main_quit()

def kill_stale_qemu():
    """Kill any leftover QEMU processes so ISO write-locks are released."""
    try:
        result = subprocess.run(["pgrep", "-x", "-f", "qemu-system"],
                                capture_output=True, text=True)
        for pid in result.stdout.strip().splitlines():
            try:
                os.kill(int(pid), signal.SIGKILL)
            except Exception:
                pass
    except Exception:
        pass

def main():
    kill_stale_qemu()
    win = EssoraVM()
    Gtk.main()

if __name__ == "__main__":
    main()
