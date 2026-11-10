---
title: "How to Customize a MikroTik Hotspot Login Page with AI | Custom Login Template"
date: 2026-10-02
slug: how-to-customize-a-mikrotik-hotspot-login-page-with-ai-custom-login-template
categories: ["MikroTik", "AI×Networking", "Youtube Videos"]
youtube_id: GSPEagKNJDQ
description: "In this video, I show you how to customize a MikroTik HotSpot login page and replace the default login screen with a clean, modern, branded design. MikroTik HotSpot is a useful feature for providing authenticated Wi-Fi access."
---

The default MikroTik Hotspot login page works. It just looks like a default page. If the Wi-Fi belongs to your company, your cafe, or your restaurant, the login page should look like it belongs to you: your logo, your slogan, your social links, and your services as a menu.

You can do that by editing a little HTML and CSS. And if HTML and CSS are new to you, you can do it with AI. This lab shows both ways.

## What We Are Building

A custom Hotspot login page for a MikroTik router, with a modern dark design, social links, and a working login form. The plan:

- Look at the files MikroTik generates for the Hotspot
- Edit the login page by hand, to learn the structure
- Generate a full new design with AI
- Upload it to the router and test login
- Know how to reset everything if it breaks

I already have a Hotspot server running on this router, with one server profile and one Hotspot account. This video does not cover setting up a Hotspot server from scratch. If you need that, let me know in the comments.

## Before You Start

You need a working Hotspot server, WinBox, and a text editor. I use VS Code. For the AI version you also need a chat AI. I use ChatGPT in this video, but any AI works.

One thing to know first: when you create a Hotspot, MikroTik automatically generates the files for the pages users see: the login page, the logout page, the status page, and more.

## Step 1: Look at the Hotspot Files

I log in to the router with WinBox and open IP, then Hotspot. One Hotspot server is active, and its profile is there.

In the Files menu, I open the hotspot directory. Inside it are HTML pages, a JSON file, a CSS file, and one JavaScript file for the functionality. There are two images, and a subdirectory with more HTML pages.

When users try to log in, they see the default login page. We all know it. We want to replace it with our own design.

The procedure is simple. Download the hotspot directory to your computer, change the HTML and CSS, and upload it back to the router.

## Step 2: Edit the Login Page by Hand

First I do a small manual edit, so the structure is clear. I download the hotspot directory to a folder on my desktop and open it in VS Code. All the directories and files are there.

I open login.html. The HTML code is on one side, the preview on the other. I also check the status page the same way, and look at the other files, including the favicon and the images under the img folder.

Then I change two lines of text in the login page, save the file, and go back to WinBox. I delete the hotspot directory on the router and upload my edited one instead.

I refresh the page in Chrome. The changes are applied. The edited text shows up on the login page.

Expected result: the login page shows my edited text. The structure works, and a small edit is enough to prove the workflow.

## Step 3: Generate a New Design with AI

A small text edit is fine, but a great login page needs a real design: modern, minimal, and responsive. For that I use AI, and I do not need to know HTML or CSS.

I prepared a prompt in advance and I share it on my Telegram channel. The link is in the video description. You can use my prompt and change it, or write your own. The prompt is the whole skill here. A good prompt is what makes AI understand what you actually want.

First I zip the hotspot directory and upload it to ChatGPT, together with the prompt. ChatGPT reads the existing files, so the login form keeps working, and builds a new design around them.

After a few seconds ChatGPT gives me a new ZIP file, with a short description of what it changed. I download it and extract it. I remove everything except the hotspot folder and rename it to "hotspot".

I open it in VS Code. The design is dark, it has my social links, and it looks good. The status page is redesigned too.

I used ChatGPT here, but you can use Gemini or any other AI. I prefer Figma Make for this kind of work. It is specialized in front-end design and creates a better design. The tool is your choice. The workflow is the same.

Expected result: a complete hotspot folder with a new design, login form intact.

## Step 4: Upload the New Pages and Test

Back in WinBox, I delete the hotspot directory on the router and upload the new one.

Then I refresh the browser. The status page shows first, since I am already logged in. I log out, and the new login page appears. It looks great.

I check responsiveness in Chrome DevTools, on an iPhone 16 size. The login page holds up on a small screen.

Then I test the part that matters most: the functionality. I log in with my Hotspot user. It works.

Expected result: the new login page loads, it fits a phone screen, and login works with a real Hotspot user.

## If You Break It: Reset HTML

Do not be afraid of messing up these files. You can reset everything with one button.

In WinBox, open IP, then Hotspot. On the first tab, select the server and click Reset HTML. Everything goes back to the default pages.

I tested this in the video. After the reset, I refresh the page and the default HTML and CSS are back. Nothing is lost that cannot be restored.

## Final Thoughts

This is one of the easiest wins on a MikroTik router. The Hotspot already generates all the pages. You download a folder, change it, and upload it back. AI removes the last barrier, which is knowing HTML and CSS.

Two things to keep in mind. First, always test the login after you upload a new design. A page can look perfect and still have a broken form. Second, keep the reset button in mind, and do not be afraid to try a design. The default pages are one click away.

The result is a login page that looks like your business, not like a default router page. For a cafe, a restaurant, or a company guest network, that is worth the ten minutes it takes.

## Official Documentation

- [MikroTik Hotspot Customisation](https://manual.mikrotik.com/docs/authentication-authorization-accounting/hotspot-captive-portal/hotspot-customisation/)
