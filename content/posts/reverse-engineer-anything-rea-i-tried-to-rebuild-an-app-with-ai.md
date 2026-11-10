---
title: "Reverse Engineer Anything (REA): I Tried to Rebuild an App with AI"
date: 2026-10-23
slug: reverse-engineer-anything-rea-i-tried-to-rebuild-an-app-with-ai
categories: ["AI×Networking", "Youtube Videos"]
youtube_id: pDUvMR2gx_c
description: "Can AI reverse engineer an application without its original source code and build a similar one? That's what I wanted to test using Reverse Engineer Anything (REA), an open-source GitHub project, and Claude Desktop."
---

You have an app on your computer. It works. You open it, you use it, and that is fine. But you do not have its source code. So here is the question: can AI look at that app, figure out how it works, and build another one like it?

That is what I wanted to test. I used an open-source project called REA, short for Reverse Engineer Anything, connected it to Claude Desktop, and handed Claude a real app installed on my Mac. Then I asked it to rebuild that app without touching the original source code.

## What REA Is

Reverse engineering is not a new idea, and the tools for it are not new either. Ghidra and Hopper have done this work for years. REA is not another AI model, and it is not a replacement for those tools.

The idea is simple. REA connects reverse engineering tools to an AI agent. It hands the tools to the agent, and the agent uses them to inspect an application, look at the code, and collect evidence about how the app actually works. The tools connect to the agent through MCP, the Model Context Protocol, which is how AI agents talk to external tools.

The important part is that the agent decides what to investigate next, based on what it already found. It is not one command and one result. It is a process.

The flow looks like this:

1. **Ask.** You give the agent a prompt: investigate this feature in this app, and build the same feature for me.
2. **Investigate.** The agent uses REA to look at the binary files, the functions, and the other files that belong to the app.
3. **Read the evidence.** REA keeps the results: code, function information, references, and other details about the app.
4. **Use what you learn.** The agent uses that evidence to explain the feature, or the whole app logic, and to build something from it.

And when the agent does not have enough information, it asks another question and investigates more. It can go back for the logic, the UI, or whatever is missing.

## Before You Start

You need Node.js and npm on your system first. I already had both installed, so I checked them with:

```
node --version
npm --version
```

Both printed a version, so I was ready. If you run Windows or Linux, the Node.js docs cover the install for your system.

One more thing to be clear about before the test. The app I picked is Paintlet, a free image editor for macOS, a lot like Windows Paint. It has a pencil, a paint bucket, a color tool, and shapes. Paintlet is open source, but I did not use its source code for this test. I installed it on my Mac and treated it as a closed app. You can run the same test on any app you want, paid or free.

## Step 1: Install REA

The install command comes from the REA repo:

```
npx rea-agents setup
```

The installer asks a few questions. First, which AI agent you want to use. The list includes Claude Code, Claude Desktop, Codex, Cursor, and others. I picked Claude Desktop to keep it simple.

Then it asks about installing the REA skill for that agent, and about installing Hopper. Hopper is one of the tools REA can use for binary analysis, so I said yes. Hopper opened and asked for a license, and I picked the demo option. In the end I did not need Hopper open for this test. The work happens when I give Claude the prompt.

Expected result: REA is registered with your agent, and the agent is ready to take the prompt.

## Step 2: Give Claude the Prompt

I opened Claude Desktop and wrote a short prompt. It said, in plain words: use the REA skill to reverse engineer the Paintlet app installed on my Mac, analyze everything about it, and do not use its GitHub source code. Then, based on the findings, build a macOS desktop app with similar functionality.

I added one more line on purpose: do not create an HTML artifact. Before this recording I had tried a similar prompt, and Claude built a web app instead of a desktop app. I wanted a real macOS app this time.

Expected result: Claude starts the investigation and asks for the permissions it needs.

## Step 3: Allow the Permissions

Claude asked for access to Paintlet, Finder, and Terminal, and it gave a reason for each one. I allowed all of them for this session. Then it asked for access to a few more locations on the disk, and I allowed those too.

This is the part where you wait. The agent is working through the app on its own, deciding what to check next.

## Step 4: Check What Claude Built

About 10 to 15 minutes later, Claude had already created a new application. After 28 minutes it reported that the app was done. It named it Paintbox, and it described it as a native Swift AppKit paint app, built from what it found inside Paintlet.

So I opened both apps side by side and tested the new one. The UI looked good to me. It uses dark mode, and I think it looks better than the original. The zoom works. The tools work. I changed the color, and that worked. Undo and redo worked too.

For a simple app like this, I call that an acceptable result. But I did not test every feature and every function. It worked on the parts I checked, and that is all I can say.

## One Limitation I Found While Testing

REA is not a tool that magically recovers the original source code of an app. It does not mean Claude can rebuild every program perfectly.

For this app, it worked. For a more complicated app, there could be drift, problems, and bugs in the result. The quality of the result depends on three things: the app itself, the tools available, and how well the agent understands the evidence.

That difference matters. There is a real gap between an interesting demo and a reliable engineering tool. This was a simple paint app. Now think about cloning something like Adobe Premiere Pro or Adobe Photoshop. That is a different question, and this test does not answer it.

## Final Thoughts

I like what this test showed, but I want to keep the scope honest.

REA gives an AI agent access to tools that help it investigate software. Instead of checking everything by hand, the agent uses the evidence to decide what to look at next. That works, and it worked on a real app here.

It also raises a fair question for software developers. If AI can help us understand existing software and build a similar app, some development tasks will get faster and easier. Simple features may become less valuable.

But I do not think software engineering becomes less important. Writing code is only one part of building software. We still need good architecture, security, testing, maintenance, and systems that actually work in production. As AI gets better at writing code, understanding systems and products, checking, testing, and security become more important day by day, not less.

Try it yourself, on a more complicated app if you like, and share your result in the comments.

### Official Documentation

- [REA on GitHub](https://github.com/morluto/rea)
