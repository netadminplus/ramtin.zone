---
title: "MikroTik ROSE Storage: Mount a Windows Share (SMB) on RouterOS! | NO STORAGE LIMITS HACK 🔥"
date: 2025-11-20
slug: mikrotik-rose-storage-mount-a-windows-share-smb-on-routeros-no-storage-limits
categories: ["MikroTik", "Windows", "Youtube Videos"]
youtube_id: ogN3AVqONtY
description: "In this MikroTik tutorial, I address a common challenge for many RouterOS users: limited internal storage. You will learn how to install the specialized ROSE (RouterOS Enterprise) package and configure its SMB feature to mount a Windows Shared Folder directly onto your MikroTik device."
---

Most MikroTik routers have tiny onboard storage. That means no space for large files and no space for a personal media server on the router. If your device has a USB port, you plug in a disk and move on. If it does not, you were stuck.

My lab router is a hAP ax lite. It has 128 MB of storage and no USB port. That is not enough for backups from other systems, and it is not enough for a media server the family can stream movies from.

MikroTik has a fix for this, and it needs no hardware at all: the ROSE package. ROSE lets the router mount a Windows shared folder over the network and use it as its own storage.

In this lab, I install ROSE on the hAP ax lite and mount a Windows share from my file server, then stream a movie from it.

This video continues the earlier DLNA media server video, where I set up the media server itself. Here we fix the storage problem underneath it.

## What We're Building

ROSE stands for RouterOS Enterprise. It is a package that adds data-center storage features to RouterOS: disk monitoring, improved formatting, RAID, rsync, iSCSI, and more.

The feature we need is SMB. SMB is Server Message Block, the file-sharing protocol Windows uses. With ROSE, RouterOS can connect to a Windows share as a client, read from it, and write to it, following the permissions set on the Windows share. The router then sees that network folder as one of its own disks.

The share in my lab sits on a Windows machine at 192.168.88.254, in a folder called `silo`, holding media files.

## Before You Start

Check two things before you install anything.

First, ROSE only runs on ARM, ARM64, x86, and TILE. My hAP ax lite has an ARM CPU, so it qualifies. Check your own device in System, then Resources, before you download anything.

Second, back up your configuration. Installing a package means a reboot, and a backup costs a minute.

You also need the share ready on the Windows side: a shared folder, a username, and a password the router can use.

## Step 1: Install the ROSE Package

My router runs RouterOS 7.20.2. In System, then Packages, there is no ROSE package yet, so I need to download it for this exact version.

Open the MikroTik website, go to the download archive, find version 7.20.2, and download the all-packages zip for the ARM CPU. Extract it, find the rose-storage package, and drag and drop it into WinBox.

Wait for the upload, then reboot the router. After the reboot, open System, then Packages again. The rose-storage package is now in the list.

Expected result: the package shows as installed, and the router has a new `/disk` menu with the ROSE features.

## Step 2: Mount the Windows Share

The command is short. Before running it, check the current disks:

```
/disk print
```

There is nothing there. Now add the SMB disk:

```
/disk add type=smb smb-address=192.168.88.254 smb-share=silo smb-user=ramtin smb-password=<your-share-password>
```

The properties are the address of the machine holding the share, the share name, and the Windows username and password. Change the address, share name, and credentials to match your own setup.

Run `/disk print` again. The SMB share is now in the list.

Then open Files. The `silo` directory is there, with the files from the Windows share inside it. The router still has its own 128 MB, but the files on the share are far bigger. Two of them are over 1 GB each. That is the whole trick: the storage limit is now the size of the share, not the size of the router flash.

Expected result: `/disk print` shows the mounted share, and Files shows the shared directory with its contents.

## Step 3: Check the Media Server and Stream

Open IP, then Media. A media server is listed there, holding the SMB files from the `silo` directory. The media server itself came from the earlier DLNA video; the new part here is the storage behind it.

To test it, I used my phone, connected to the router Wi-Fi. I opened VLC, went to the browse tab, and the MikroTik media server was there. I opened one of the episodes from the share and played it. The stream started and played well, limited only by the network speed.

Expected result: the media server lists the shared files, and a phone on the router Wi-Fi plays them.

## What Else This Is Good For

Media is the demo, but the mounted disk is general storage. The same share can hold backups from other systems, files downloaded straight to the router, or logs that need more room than 128 MB allows.

The ROSE package has more features behind this one, like RAID and iSCSI. This video covers SMB only, because that is the one that fixes the missing-USB problem with no hardware.

One detail from the docs: ROSE speaks SMB 2.1, 3.0, and 3.1.1. SMB1 is not supported, for security reasons. If your share only speaks SMB1, this will not connect.

## Final Thoughts

A hAP ax lite with 128 MB and no USB port is not a storage device. With one package and one command, it borrows the disk of a Windows machine on the same network, and the media server on top of it just works.

It is not magic, and the title is not literal: the storage is limited by the share, not by the router. But going from 128 MB to a full shared folder, with no hardware purchase and no USB port, is a fair trade for a home setup.

Check your CPU architecture first, back up before installing, and the rest is one mount command.

## Official Documentation

- [ROSE Storage — MikroTik Documentation](https://help.mikrotik.com/docs/spaces/ROS/pages/259031065/ROSE-storage)
