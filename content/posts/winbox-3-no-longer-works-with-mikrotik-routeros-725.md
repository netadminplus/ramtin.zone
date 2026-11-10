---
title: "WinBox 3 No Longer Works with MikroTik RouterOS 7.25!"
date: 2026-10-28
slug: winbox-3-no-longer-works-with-mikrotik-routeros-725
categories: ["MikroTik", "Youtube Videos"]
youtube_id: _s6EfRB2lPo
description: "With the release of MikroTik RouterOS 7.25, WinBox 3 can no longer connect to routers running this version. MikroTik now requires WinBox 4.3 or newer. In this video, I explain what changed in RouterOS 7.25, why WinBox 3 is no longer compatible, and what MikroTik administrators need to know before upgrading their routers."
---

If you manage MikroTik routers with WinBox 3, your next RouterOS upgrade is going to break your workflow.

Upgrade a router to RouterOS 7.25, try to open it with WinBox 3, and you get an error: the router requires a newer WinBox. There is no setting to change and no workaround. MikroTik ended WinBox 3 with one line in the 7.25 changelog: the minimal supported WinBox version is now 4.3.

Version 3.43 is the last WinBox 3. It still works on RouterOS 7.24 and older, and on RouterOS 6. But anything on 7.25 or newer needs WinBox 4.3 or newer.

## What you need

- WinBox 4.3 or newer. At the time of recording, the latest version is 4.4.
- A router on RouterOS 7.25, or one you plan to upgrade.

WinBox 4 is a full rewrite, not a reskin. Like WinBox 3, it is portable: there is nothing to install, you just run it. Unlike WinBox 3, it runs natively on Windows, macOS, Linux, and Windows ARM. You can download it from the MikroTik download page, under Tools.

## Step 1: See the break for yourself

Open the RouterOS 7.25 changelog and search for "minimal". The line is there: the minimal supported WinBox version is 4.3.

Now try it. In the video I connect with WinBox 3 to a router on RouterOS 6.49 and to one on RouterOS 7, and both work. Then I try the router on 7.25, and WinBox 3 refuses with the "router requires newer WinBox" error.

That is the whole change. Nothing else in your configuration is involved.

## Step 2: Get WinBox 4

On the MikroTik download page, open the Tools tab and then WinBox. Pick the build for your platform. It is the same portable application you are used to: no installer, just run it.

Connect to the 7.25 router with WinBox 4, and it works.

## Step 3: Check your saved routers

This is the part most people worry about, and on the same computer there is nothing to do.

Open the Saved tab in WinBox 4. All your routers are already there. WinBox 4 reads the same saved-routers database that WinBox 3 created, the addresses.dat.cdb file. On Windows it lives in the MikroTik folder under your roaming application data.

So if you manage a lot of routers, or routers for clients, you do not need to export anything or type anything again. It is all there.

## Step 4: Moving to another computer

Moving to a different computer is the one manual step.

In WinBox 3, use File, then Save As, and save the .cdb file. Copy it to the new computer, and in WinBox 4 use the Import button and select the file. Your routers show up.

One thing to know: the .wbx file from WinBox 3's Tools, then Export, does not work in WinBox 4. Use the .cdb file from Save As.

## Final thoughts

WinBox 3 served MikroTik users for around a decade, and it is done. New features are built for WinBox 4 only. The next one is CMR, the central controller for your MikroTik routers, which is coming with RouterOS 7.26.

If you are still on WinBox 3 for your day-to-day work, now is the time to move. The upgrade itself is simple: download WinBox 4, connect, and your saved routers are already there.

## Quick reference

- RouterOS 7.25 and newer: WinBox 4.3 or newer required
- Last WinBox 3 version: 3.43 (works up to RouterOS 7.24.x and on RouterOS 6)
- WinBox 4 at the time of recording: 4.4
- Saved routers file (Windows): %APPDATA%\MikroTik\WinBox\addresses.dat.cdb

## Official MikroTik documentation

- [WinBox download page](https://mikrotik.com/download/winbox)
- [RouterOS changelog](https://mikrotik.com/download/changelogs)
