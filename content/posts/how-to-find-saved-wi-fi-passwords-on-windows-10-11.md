---
title: "Forgot Your Wi-Fi Password on Windows 10 & 11? Here’s How to Find It on"
date: 2026-02-12
slug: how-to-find-saved-wi-fi-passwords-on-windows-10-11
categories: ["Tips & Tricks", "Windows", "Youtube Videos"]
youtube_id: O5wegipxt6E
image: /assets/images/how-to-find-saved-wi-fi-passwords-on-windows-10-11-netadminhub.com_.webp
description: "We’ve all been there: a friend comes over and asks for the Wi-Fi password, and suddenly your mind goes blank. You’re already connected, so you…"
migrated_from: netadminhub.com
---

We’ve all been there: a friend comes over and asks for the Wi-Fi password, and suddenly your mind goes blank. You’re already connected, so you don’t usually think about it—until you need to connect a new device.

In the old days of Windows 7, finding these passwords was straightforward. But for retrieve wifi password windows 10 and 11, Microsoft hidden things a bit deeper. Today, I’ll show you two very simple ways to get that password back—one for the network you’re currently on, and a “pro” trick for any network you’ve ever connected to.

Watch the full video walkthrough on the **Net Admin HUB** YouTube channel:

## Method 1: The Quick Way (Current Connection)

If you’re already connected to the network and just need to see the key, the Control Panel is your best friend.

1. Open the **Control Panel** and head to **Network and Internet > Network and Sharing Center**.
1. Click on your Wi-Fi name (the blue link next to “Connections”).
1. In the window that pops up, click **Wireless Properties**.
1. Go to the **Security** tab and check the box that says **Show characters**.

There it is! But what if you aren’t currently connected to that specific network? That’s where Method 2 comes in.

## Method 2: The “Aha!” Way (Using CMD)

This is my favorite method because it works for *any* Wi-Fi profile saved on your laptop, even if the router is miles away. We’re going to use a built-in tool called `netsh`.

Instead of just giving you a long command to copy-paste, I want to show you how it works so you actually remember it.

1. Open your **Command Prompt (CMD)**.
1. Type `netsh wlan show profiles` to see a list of every Wi-Fi network your PC remembers.
1. Once you see the name of the network you need, type this command:

```
netsh wlan show profile name="YourWiFiName" key=clear
```

Look at the **Security settings** section under **Key Content**. That is your password in plain text.

## Summary of Methods **Scenario****Best Method****Why?****Currently Connected****Not Connected / Forgotten****Pro Tip**

|  |  |  |
| --- | --- | --- |
|  | Control Panel | Visual and easy to navigate. |
|  | CMD (netsh) | Accesses all saved profiles instantly. |
|  | CMD (netsh) | No need to click through multiple menus. |

### Final Thoughts

It’s a bit frustrating that Microsoft made this harder to find find wifi password windows 10 and 11, but once you know the `netsh` trick, you’ll never feel “locked out” of your own saved passwords again.

If this helped you out, I’d love to hear about it! Feel free to check out my other quick Windows and Networking tips on ********[Ramtin Tech Zone YouTube Channel](https://youtube.com/@ramtintechzone) or join our Farsi community at **[NetAdminPlus](https://youtube.com/netadminplus)**.
