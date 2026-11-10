---
title: "Turn Your MikroTik Router Into a Powerful DLNA Media Server! (Easy Home Streaming Guide) 🔥"
date: 2025-11-17
slug: turn-your-mikrotik-router-into-a-powerful-dlna-media-server-easy-home-streaming
categories: ["MikroTik", "Youtube Videos"]
youtube_id: 2NemslWUWU4
description: "In this MikroTik tutorial, you will learn the essential steps to configure the powerful, built-in DLNA Media Server feature, turning your MikroTik router into the ultimate home media hub!"
---

Tired of moving USB sticks and cables around just to get a movie onto the bigger screen? Your MikroTik router can fix that. RouterOS has a built-in DLNA media server, and once it is set up, your smart TV, phone, tablet, and laptop can find your movies, music, and photos on the network and play them straight from a USB drive plugged into the router.

In this lab I set it up on an old RB951, added a second server just for the kids, and then locked the main server so only one laptop could see it.

## What We Are Building

- **One DLNA server** for the whole family, sharing the videos on a USB drive.
- **A second DLNA server** that only shares the kids' animations.
- **An IP limit** on the first server, so the kids' TV never sees the rest of the library.

The clients find the servers by themselves. No app to install on the TV, no file sharing to configure on each device. VLC on Windows and VLC on Android both picked the servers up on their own.

## Before You Start

Three things to check first, in System, then Resources in WinBox.

**RouterOS version.** The DLNA server needs RouterOS v7.14 or newer. Update first if you are on an older version.

**CPU architecture.** My RB951 runs MIPSBE, and that is fine. The one architecture that does not work is SMIPS. If your router has a SMIPS CPU, you cannot use this feature.

**Storage.** My router only has about 100 MB of free disk space, and that is nowhere near enough for a media library. I plugged a USB stick into the router's USB port. If your router has no USB port, there is another way: the ROSE package, short for RouterOS Enterprise, lets the router use a shared folder on a Windows machine as extra storage. I used the USB drive in this lab. If you want a video about the ROSE way, tell me in the comments.

## Step 1: Format the USB Drive

Go to System, then Disks. My drive shows up as USB 1, with about 32 GB of space.

Format it as exFAT. WinBox also offers FAT32, but FAT32 cannot hold a single file larger than 4 GB, and a 4K movie will pass that limit fast. exFAT is the better choice here.

After a few seconds the file system is created. Then go to Files. USB 1 shows up there as a disk. Drag and drop your media files into it. I dropped in two video files.

Expected result: the drive is formatted as exFAT, and the files sit under USB 1 in Files.

## Step 2: Create the First Media Server

Go to IP, then Media, and click Add. There are four fields that matter:

- **Interface:** the interface your users are connected to. In my setup that is the default bridge, and all the ports sit under it. Pick the right interface for your own setup.
- **Path:** the folder that holds the media. For me that is `usb1`.
- **Friendly name:** the name your family sees on the network. I named it DLNA.
- **Allowed IP / Allowed hostname:** leave these empty for now. We use them in Step 4.

Click Apply. The server shows as running.

The same settings exist on the command line, from the MikroTik manual:

```
/ip media add friendly-name=Mikrotik interface=bridge1 path=usb1
```

Expected result: the server is running, and any DLNA client on the LAN can find it.

## Step 3: Test It on VLC

Open VLC on a Windows machine. Go to View, then Playlist, or press Ctrl+L. Under Universal Plug and Play, the MikroTik DLNA server shows up. Open it, and the files are there. Play one, and the video plays.

The same works on a smart TV. The TV scans the network, finds the server, and streams the media. The setup is done at this point, and it really is that short.

## Step 4: Add a Kids Server and Limit the Main One

Now the part that makes this useful for a family. I have kids at home, and I want their TV to see only their animations, not the whole library.

First, make a folder for the kids. In Files, create a directory called `kids` under USB 1, and move one video into it, an animation.

Then go back to IP, then Media, and create a second server. Same interface, the bridge. The path is `usb1/kids`. I left this one open, with no limits. Back in VLC, a second DLNA server appears, and it holds just the one animation.

Now limit the first server. I need the laptop's IP address, so I ran `ipconfig` on the Windows machine. Then, in IP, then DHCP Server, on the Leases tab, I made the laptop's lease static, and I made the phone's lease static too. Treat that phone as the kids' smart TV for this test.

Then I edited the first media server and set its Allowed IP to the laptop's address only.

Expected result: on the Windows laptop, VLC still shows both servers. On the phone, VLC in Browse, under Local Network, shows only one MikroTik server, the kids' one, with just the one animation in it. Open it, and it plays. The kids can watch their animations and nothing else.

## One Limitation I Found While Testing

The DLNA server settings give you only one kind of control: which device can see which server, through the allowed IP and allowed hostname fields. There is no user or password field in the settings, and the manual lists no login option. That is why the setup above uses two servers instead of one. If you need real access control on the files themselves, DLNA is the wrong tool. Keep that in mind before you put anything private on it.

## Final Thoughts

This is a good use for an old router. A USB stick, a few clicks in WinBox, and the router becomes the media hub for the house. The kids' split took two extra steps, and it worked on the first try.

Two things to keep in mind. First, performance. Streaming high bitrate media like 4K depends on your router's CPU power and on your network. Devices with Wi-Fi 6, like the MikroTik hAP ax series, will give you a clearly better result than an old router like my RB951.

Second, if you need more than DLNA, look at the ROSE package. It adds file sharing like SMB, so you can mount a shared Windows folder as local storage on the router. That is a different setup, and it is worth a video of its own.

### Official Documentation

- [MikroTik DLNA Media Server Documentation](https://help.mikrotik.com/docs/spaces/ROS/pages/237699479/DLNA+Media+server)
