---
title: "MikroTik ROSE Storage: Mount a Windows Share (SMB) on RouterOS! | NO STORAGE LIMITS HACK 🔥"
date: 2025-11-20
slug: mikrotik-rose-storage-mount-a-windows-share-smb-on-routeros-no-storage-limits
categories: ["MikroTik", "Windows", "Youtube Videos"]
youtube_id: ogN3AVqONtY
description: "In this MikroTik tutorial, I address a common challenge for many RouterOS users: limited internal storage. You will learn how to install the specialized ROSE (RouterOS Enterprise) package and configur"
auto_generated: true
---
In this MikroTik tutorial, I address a common challenge for many RouterOS users: limited internal storage. You will learn how to install the specialized ROSE (RouterOS Enterprise) package and configure its SMB feature to mount a Windows Shared Folder directly onto your MikroTik device. This technique effectively expands your router's disk capacity, allowing you to use the external network share for hosting large files, DLNA/Media Server content, or network backups (especially useful for models like the hAP ax lite that lack a USB port).

In this tutorial I walk through the whole setup step by step — what it is, what you need before you start, and the exact configuration that works. The video above shows the full lab; below is the written reference so you can follow along or copy the commands.

## What you will learn

- Introduction: The MikroTik Storage Limitation (The USB Port)
- The Solution: Introduction to the MikroTik ROSE Package
- How to Download and Install the MikroTik ROSE Storage Package
- Configuring MikroTik SMB Mount via Terminal Command (disk add)
- Verifying the Mounted Windows Share and Accessible Files
- Confirming MikroTik Media Server Auto-Creation
- Live Test: Streaming from MikroTik to Mobile App (VLC)
- Final Thoughts

## How it works

Kind: captions Language: en Hey, if you're a micro user, you know the struggle. Most of these routters onboard disk storage is tiny. That means there is no space for storing large files and no space for setting up a personal media server on your router. For a long time, if your uh device didn't have a USB port, you were stuck. But now, Microic has a powerful solution, the ROS package. In the previous video, I showed you how to set up a personal media server on your Micro Micro router. In this video, I'm going to show you how to install ROS package on your routter and use its SMB feature to mount a Windows shared folder from your file server directly to your Microick router. Uh, this lets us instantly and massively expand our routters storage capacity for any use case, all without any physical hardware upgrades. Here you can see I have a microic router inside my home network and the model is half AEX light and like most of microic routters it doesn't have enough disk storage. Maybe I need to store some backups from other systems on this router. Or maybe I just need to set up a media server for my family and they need to stream some movies on the home's smart TV from my media server.

But the problem is this specific router doesn't have USB interface. I can't connect a USB disc to this router and increase its capacity. Here you can see uh the name is rose storage and rose stands for router OS enterprise. This package adds some data center functionality to router OS for example disk monitoring improved formatting raid rs sync is some other stuff here but it just supported on these CPU architectures ARM ARM 64 and x86 and also tile here in my winbox you can see in system and then resources and my CPU architecture is ARM the board name is HA aex light and you can see my HD size is only 128 mgabytes. We need to install a rose uh package on this router and connect it to a share directory in the network. You can see some documentation about uh different functionalities on this package. But uh here we we are just covering SMB uh which is a server message block. It is a popular file sharing protocol which is completely supported by Windows systems and with this rose package micro completely support SMB protocol and it can connect to a Windows share directory for example to my file server and it can use that disk space too and it can write on the disk and it can read from it based on the permission you have provided in the windows share. Uh we can resolve this problem with this interesting package. First of all, we need to install the package on the router here in the win box. I need to download this package for my specific version.

Let's open uh micro website here and head to software tab under the download archive. I need to find my specific um version under ARM CPU. And from the directory, I need to drag and drop rose storage package to my vimbox. Now wait for uploading and now I need to reboot my router. The router is rebooted and here in system and then packages I can see here the rose storage and now I can easily connect this microick router to a windows share and the command is very easy and straightforward. Here you can see the command and you can easily copy and paste it and change the IP address and share name here. And there are some uh properties which is needed here. The IP address of the device which holds the share folder or windows password, Windows username and directory name. And you can see my uh Windows IP address is 88 uh 254. SMB- address is 192.168.88.254 and uh the next one is SMB share name I mean the directory here the directory here is silo okay so uh SMB- uh share name is silo and the next one is SMB user SMB- user is romin and the password is SMB- password is one let's hit enter and it's done and now I can get the report again And you can see the SMB share here. If I open the file here, you can see uh the silo directory and the uh size of the files inside that that directory.

We successfully connected our router to a share directory on our file server inside our network. But first let me show you here in IP and then media. You can see it dynamically created a media server on this router uh which holds the SMB files here this directory silo here. On my mobile which is connected to this uh microix Wi-Fi um I need to open VC and in the browse tab I can see the microick uh media server here and for example open this one. This is one of the episodes of this series on the share directory. And based on the network speed, you can see the stream will start and is working very well. We successfully installed the ROS package and configured the SMB mount effectively upgrading our Microix storage capacity. Now, as you saw, we can now use the shared disk space to host some media files and enable a DNA media server. Or maybe you just want to download some files directly on your microick itself. Did you ever try a different feature of this rose package, for example, RAID or iskazi? If you're interested into a video covering those features, too.

## Wrapping up

If this helped, subscribe to Ramtin Tech Zone on YouTube for more MikroTik, Linux, networking, VPN and AI tutorials — and if a script or tutorial saved you time, consider supporting the work on the Donate page.
