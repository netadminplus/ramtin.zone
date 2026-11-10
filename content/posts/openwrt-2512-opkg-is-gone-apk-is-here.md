---
title: "OpenWrt 25.12: OPKG is Gone, APK Is Here!"
date: 2026-09-10
slug: openwrt-2512-opkg-is-gone-apk-is-here
categories: ["OpenWrt", "Youtube Videos"]
youtube_id: fl99lo_5GLs
description: "OpenWrt 25.12 brings some important changes, including one of the biggest changes in recent OpenWrt releases: the move from OPKG to APK. In this video, I take a look at what's new in OpenWrt 25.12, what these changes mean in practice, and what you should check before upgrading your router."
---

OpenWrt 25.12 has been out for a while, and it brings some big changes. The biggest one is the package manager moving from OPKG to APK. If you use terminal commands, install packages, or run your own scripts on your router, that matters for you.

There are also improvements to the upgrade process, changes under the hood, new hardware support, and updated core components. In this video, I cover the key changes, what they mean in practice, and what to check before upgrading your device.

The main question is simple: should you upgrade your device now, or wait?

## First, What 25.12 Is

OpenWrt 25.12 is a new major stable release series. If you run OpenWrt 24.10 or older, 25.12 is the next major version for you. Versions like 25.12.1 or 25.12.2 are updates inside this series. They bring bug fixes, security fixes, and other improvements.

This video is about the bigger changes that came with the new series, not the point releases.

## The Big Change: OPKG Is Gone, APK Is Here

If you have used OpenWrt for a while, OPKG is familiar. That is how we managed packages. On a device running OpenWrt 23.05, updating the package list and installing the nano editor looked like this:

```
opkg update
opkg install nano
```

On OpenWrt 25.12, the same two jobs look like this:

```
apk update
apk add nano
```

The commands are different, but most package names are still familiar. OpenWrt also published an official opkg-to-apk cheat sheet that maps the common commands. It is worth keeping open while you switch.

Why did OpenWrt change it? The reason is simple. The OpenWrt fork of opkg is no longer maintained. OpenWrt needed a package manager that is actively maintained and can move forward with the project. APK is the package manager from Alpine Linux, and it is well known and still maintained. For OpenWrt, this is a long-term change.

One warning before you type anything new. Do not assume that upgrading packages now means typing `apk upgrade`. The OpenWrt documentation specifically warns against doing that blindly. Firmware upgrades and package upgrades need the proper upgrade tools. I cover those next.

## Who Needs to Care

It depends on how you use OpenWrt. If you mostly use the LuCI web interface and rarely touch the terminal, you will not notice a huge difference day to day.

If you connect over SSH, install packages, manage several devices, or write scripts and automate things, this change matters for you. The terminal is where OpenWrt gets much more powerful than the web interface, and your old commands and scripts will need updating. If you move to 25.12, opkg is gone, and anything that calls it stops working.

## Upgrades Get Easier: Attended Sysupgrade

The next important change is the upgrade experience, and for regular users it is one of the most useful improvements in this release.

Say you have used OpenWrt for a while. You configured the network, installed extra packages, maybe monitoring tools or VPN packages. Now you want to upgrade, and you do not want to spend time remembering every package you installed, or rebuild the whole setup after every upgrade.

Attended Sysupgrade solves that. It looks at the packages installed on your device and requests a custom firmware image that includes them. If you keep your configuration, your settings are preserved as well.

In OpenWrt 25.12, the Attended Sysupgrade application is installed by default, and devices with larger flash storage also include `owut`, a command-line tool for checking and managing upgrades.

This video does not do the actual upgrade. If you want a separate video that goes through the full process step by step, backup, compatibility check, upgrade options, and the upgrade itself, let me know in the comments. For now, the point is that moving to a new firmware version no longer means rebuilding your package setup from scratch by hand.

## Under the Hood

A few changes you will not notice right away, but are still worth knowing.

**Wi-Fi scripts rewritten in ucode.** The Wi-Fi management scripts were rewritten using ucode. You will not install 25.12 and see a different Wi-Fi interface. The goal is better performance, fewer problems, and easier maintenance going forward.

**Shell history is preserved.** Command history now survives across sessions using a RAM-backed file system. You can reconnect to the router and still have your recent commands, without writing them to flash storage every time. It is a small quality-of-life fix, but if you spend a lot of time over SSH, you will feel it.

**Core components updated.** Like any major version, 25.12 brings a newer Linux kernel, updated toolchains, updated networking components, and updated packages. The release notes list kernel 6.12.71 for all targets, dnsmasq 2.91, Dropbear 2025.89, and BusyBox 1.37.0. This is not just a release with a newer package manager. A lot of the foundation moved forward too.

## Does Your Device Support 25.12?

Before you download anything, check this. One mistake I see people make is assuming their router supports the latest version because it supports OpenWrt. Not necessarily. And even when a device supports the latest version, there can be device-specific information you need before upgrading.

Here is how I check. First, the OpenWrt Table of Hardware page. Find your exact device there, with its firmware and sysupgrade image and installation docs. My example is my own Asus router, the RT-AX53U.

Find the exact model. Do not search for something that looks similar. Router names are confusing, different hardware revisions exist, and two devices with almost identical names can be completely different inside.

Then open the device page. It has device-specific information: installation instructions, upgrade information, warnings, and known issues that might matter for your model.

Then check the Firmware Selector. Pick your version, search for the device again, and it shows the sysupgrade image, the factory image, the kernel, and the installed packages on that image.

My process is simple: check the exact device, check the device page, and check the available firmware. Do not upgrade based on assumptions. A few minutes of reading can save a lot of time later.

## New Hardware Support

OpenWrt 25.12 also adds support for new hardware. That matters because OpenWrt is not just for home routers anymore. People use it for custom network appliances, gateways, firewalls, switches, and all kinds of embedded devices.

The release supports over 2,200 devices, with over 180 new ones added on top of 24.10. At the same time, most devices supported by OpenWrt 24.10 are also supported by 25.12. But again, check your exact device and make sure there is no important known issue for your model.

## OpenWrt 24.10 Reaches End of Life

If you run OpenWrt 24.10, there is one more thing to know. The 24.10 stable series was scheduled to reach end of life in September 2026. After that, it gets no more security updates.

That September 2026 date has now passed, so a router still on 24.10 gets no more security updates. That does not mean you need to panic and upgrade this second, but you should have a plan, especially if your device faces the internet, works as a firewall, or sits as an important gateway in your network. Staying on an unsupported release long-term is not a good idea, because security updates matter.

## Should You Upgrade?

My answer is probably yes, but do not upgrade blindly.

Consider upgrading now if your exact device is supported, you checked the device page, there is no important known issue for your model, you checked your installed packages, and you understand that OPKG has been replaced by APK. If you run scripts that use the package manager, they need changing. Your setup should also be something that can handle a possible interruption.

If you set up a new OpenWrt device today, 25.12 is the version I would seriously consider.

Wait and test first if your setup is heavily customized, you use a lot of extra packages, you have your own scripts, and those scripts depend on OPKG commands. In that case, do some testing before upgrading, and make sure everything you depend on actually works.

Before upgrading, here is the checklist I follow:

- Check your exact device
- Read the device page
- Check the available firmware
- Check your installed packages and scripts
- Create a backup
- Read the release notes

A few minutes of preparation can save you from a lot of problems.

## Final Thoughts

OpenWrt 25.12 is a real step forward, and the APK switch is the change that will touch the most people. The upgrade tools got better at the same time, which softens the move, and the core underneath is newer across the board.

The risk is not the release itself. It is upgrading without checking the device, the scripts, and the backup first. Do those three things, and 25.12 is a good place to be.

## Official Documentation

- [OpenWrt 25.12.0 Release Notes — GitHub](https://github.com/openwrt/openwrt/releases/tag/v25.12.0)
- [OpenWrt Firmware Selector](https://firmware-selector.openwrt.org/)
