---
title: "Host a Website for FREE with Cloudflare | AI Website Tutorial"
date: 2026-09-18
slug: host-a-website-for-free-with-cloudflare-ai-website-tutorial
categories: ["AI×Networking", "Youtube Videos"]
youtube_id: AWpNIzRkI1Y
description: "In this video, I build a complete personal portfolio website with AI and deploy it for free on Cloudflare. The goal is to create a professional, modern, and responsive personal website without using a backend, database, CMS, or complicated build process."
---

You built a website with AI. Now it has to live somewhere. You need hosting, a domain, and HTTPS, and you would rather pay nothing for all of it.

That is the whole problem this lab solves. I build a personal portfolio website with AI, then I put it online on Cloudflare without renting a server or paying for hosting.

## What We Are Building

One static personal website. Static means HTML, CSS, and JavaScript only. No backend, no database, no CMS.

The plan is short:

- Generate the site with AI from a prompt
- Upload the files to Cloudflare Workers & Pages
- Connect a custom domain
- Check HTTPS and the DNS record Cloudflare creates
- Look at the free plan limits, and what changes for a dynamic site

I do the whole thing from scratch, so you can follow the same steps with your own information.

## Before You Start

You need two things: a free Cloudflare account, and a domain you control if you want a custom address. The domain is optional. Without one, Cloudflare still gives the site an address and it still works.

One thing to settle first: this workflow only fits a static site. If your site needs user accounts, server-side processing, file uploads, or a database, this is the wrong setup. I come back to that at the end.

## Step 1: Generate the Website with AI

I start with a prompt. It holds my personal information: my name, my title, my job background, my links, and the structure I want for the site. AI uses that as reference material to build the pages.

The prompt also sets the file structure and the expected output: a ZIP file I can download.

I paste the prompt into ChatGPT and wait a few seconds. It creates the website code and gives me a link to the ZIP file. The ZIP holds HTML, CSS, two JavaScript files, and one readme file.

I download the ZIP, extract it, and I can edit anything in it before I deploy. In this video I deploy it as it is.

Expected result: a folder with the site files, ready to upload.

## Step 2: Upload the Files to Cloudflare

In the Cloudflare dashboard I open Compute, then Workers & Pages. That is the place in Cloudflare where you create applications and websites.

I click Create application. Cloudflare offers three ways in: connect a GitHub or GitLab repo, use a template, or upload static files directly. I pick the direct upload.

I drag the ZIP file in. Cloudflare detects five files and assigns a random name to the new worker. I rename it, then I click Deploy.

After a few seconds the files are uploaded and the site is live. Cloudflare assigns it a long domain name, and the site opens on that address.

Expected result: the site loads on the Cloudflare address. I check it on a tablet size and a phone size. The layout holds up on both. The prompt asked for a responsive design, and it works.

## Step 3: Connect a Custom Domain

The long Cloudflare address works, but it is not an address you hand to visitors. So I add a custom domain.

In the worker settings I open the domain step and click to add a domain. Cloudflare lists the domains managed in my account. If your domain lives with another provider, you can still manage it inside Cloudflare. It takes a few steps.

I select my personal domain, ramtin.ir. If I leave the subdomain field empty, the site lands on the root domain. I want it on test.ramtin.ir instead, so I type "test" and click Add domain.

Expected result: the site opens on test.ramtin.ir. The browser shows the lock icon, the certificate is valid, and the certificate authority is Google Trust Services. HTTPS works with no extra setup on my side.

## Step 4: Check What Cloudflare Did in DNS

When I connect the custom domain, Cloudflare creates the DNS record for me. I check it under the domain settings, in DNS and records.

The record for test.ramtin.ir is there. Its type is "worker", it has a lock icon next to it, and it is proxied. That means visitors reach the site through the Cloudflare proxy, and Cloudflare serves the files.

Expected result: one worker-type DNS record, created automatically, proxied.

## Step 5: Publish the Next Version

Sooner or later the site changes. Maybe you edit the prompt, maybe you edit the files by hand. Either way, you get a new ZIP.

You do not create a new worker. You open the Deployments tab of the existing worker, click New deployment, and upload the new ZIP. That version is what visitors get from then on.

Expected result: the new deployment appears in the version history, and the site serves the new files.

## The Free Plan, Honestly

The free plan covers 100,000 Worker requests a day. That sounds like a hard ceiling, but requests to static assets are free and unlimited. The request limit only matters when worker code actually runs. For a normal personal site, portfolio, landing page, or company site, that is usually nothing to worry about.

There are still limits on the number of files you can deploy and the maximum size of each file. For a normal static website, those limits are more than enough.

## What This Setup Cannot Do

This is a static site. It has no backend and no database. You cannot upload WordPress, PHP, Laravel, Django, or anything like that with this workflow and expect the server-side code to run. Those applications need a backend environment.

For a custom application, you could use Cloudflare Workers together with a database or object storage service, or you could use a traditional hosting environment. That is a different setup, not this one.

## Two Things Worth Turning On

First, if you update the site often, connect a GitHub repository instead of uploading ZIP files by hand. Every time you push a new version, Cloudflare deploys it for you automatically. You touch nothing in the worker page.

Second, Cloudflare Web Analytics. In the Observability tab you can enable it and click Deploy. It shows visitors, page views, referrers, and basic traffic information, without adding a heavy analytics script to the site.

## Final Thoughts

I like this workflow because it removes the two things that usually stop people from publishing a personal site: paying for hosting, and setting up a server.

I started with an idea, used AI to build the site, uploaded the files to Cloudflare, connected a real domain, and got HTTPS without touching a certificate. No server rented, no complicated configuration.

The scope is narrow, and that is fine. For a static site, this is enough. For anything with a backend, you need a different plan. But if you are not a developer and you want a real website online, this workflow gets you there.

## Official Documentation

- [Cloudflare Pages Overview](https://developers.cloudflare.com/pages/)
- [Cloudflare Workers Pricing](https://developers.cloudflare.com/workers/platform/pricing/)
