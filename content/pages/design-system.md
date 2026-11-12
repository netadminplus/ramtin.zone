---
title: "Design System"
slug: design-system
description: "The Ramtin Tech Zone design system: tokens, components, and rules for the site's visual language."
---

This is the design system for Ramtin Tech Zone. It keeps the site consistent: one set of colors, one type scale, one spacing scale, and a small set of components. The look is modern, minimal, and dark — the same look the site already had, now written down as rules instead of one-off values.

The full documentation lives in the repo as `DESIGN_SYSTEM.md`. This page is the living reference: every token and component below is rendered with the real styles.

## Principles

- **Content first.** The article is the product. The chrome around it stays quiet.
- **Minimal, not empty.** One accent color, one surface, generous spacing. Nothing decorative for its own sake.
- **Dark by design.** The theme is dark only. No light mode, no theme switcher.
- **Tokens, not values.** No hardcoded colors, sizes, or radii in components. Everything references a token in `tokens.css`.
- **Accessible by default.** Every interactive element shows a focus ring. Text contrast meets WCAG AA.

## Colors

### Surfaces and text

<div class="ds-swatches">
  <div class="ds-swatch"><div class="ds-swatch-color" style="background:#0b0f17"></div><div class="ds-swatch-meta"><strong>--color-bg</strong>#0b0f17 · page</div></div>
  <div class="ds-swatch"><div class="ds-swatch-color" style="background:#080d15"></div><div class="ds-swatch-meta"><strong>--color-bg-deep</strong>#080d15 · footer</div></div>
  <div class="ds-swatch"><div class="ds-swatch-color" style="background:#111827"></div><div class="ds-swatch-meta"><strong>--color-surface</strong>#111827 · cards</div></div>
  <div class="ds-swatch"><div class="ds-swatch-color" style="background:#151f30"></div><div class="ds-swatch-meta"><strong>--color-surface-2</strong>#151f30 · inline code</div></div>
  <div class="ds-swatch"><div class="ds-swatch-color" style="background:#0d1526"></div><div class="ds-swatch-meta"><strong>--color-code-bg</strong>#0d1526 · code blocks</div></div>
  <div class="ds-swatch"><div class="ds-swatch-color" style="background:#1f2937"></div><div class="ds-swatch-meta"><strong>--color-border</strong>#1f2937 · borders</div></div>
  <div class="ds-swatch"><div class="ds-swatch-color" style="background:#e5e7eb"></div><div class="ds-swatch-meta"><strong>--color-text</strong>#e5e7eb · primary text</div></div>
  <div class="ds-swatch"><div class="ds-swatch-color" style="background:#9ca3af"></div><div class="ds-swatch-meta"><strong>--color-text-muted</strong>#9ca3af · secondary text</div></div>
</div>

### Accent and semantic

<div class="ds-swatches">
  <div class="ds-swatch"><div class="ds-swatch-color" style="background:#3b82f6"></div><div class="ds-swatch-meta"><strong>--color-accent</strong>#3b82f6 · actions, links</div></div>
  <div class="ds-swatch"><div class="ds-swatch-color" style="background:#60a5fa"></div><div class="ds-swatch-meta"><strong>--color-accent-hover</strong>#60a5fa · link hover</div></div>
  <div class="ds-swatch"><div class="ds-swatch-color" style="background:#2563eb"></div><div class="ds-swatch-meta"><strong>--color-accent-strong</strong>#2563eb · logo, pressed</div></div>
  <div class="ds-swatch"><div class="ds-swatch-color" style="background:#22c55e"></div><div class="ds-swatch-meta"><strong>--color-success</strong>#22c55e</div></div>
  <div class="ds-swatch"><div class="ds-swatch-color" style="background:#f59e0b"></div><div class="ds-swatch-meta"><strong>--color-warning</strong>#f59e0b</div></div>
  <div class="ds-swatch"><div class="ds-swatch-color" style="background:#ef4444"></div><div class="ds-swatch-meta"><strong>--color-error</strong>#ef4444</div></div>
</div>

## Typography

The typeface is Inter, with a system fallback. Body text is 17px at 1.65 line height. Headings are tight (-0.02em tracking, 1.25 line height).

<div class="ds-demo">
  <h1 style="margin:0 0 8px">Heading 1 — 28–42px</h1>
  <h2 style="margin:0 0 8px">Heading 2 — 26px</h2>
  <h3 style="margin:0 0 8px">Heading 3 — 21px</h3>
  <h4 style="margin:0 0 8px">Heading 4 — 18px</h4>
  <p style="margin:0 0 8px">Body text — 17px, 1.65 line height. This is how an article paragraph reads: short sentences, simple words, concrete numbers.</p>
  <p style="margin:0 0 8px; font-size:13px; color:var(--color-text-muted)">Small text — 13px, muted. Used for meta, captions, and footer text.</p>
  <p style="margin:0"><code>Inline code</code> and <code>/ip/firewall/nat</code> use the mono stack at 0.88em.</p>
</div>

## Spacing and radius

Spacing follows a 4px scale: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 72. Components use these tokens; one-off values stay literal and rare. Corners are 6px (small), 8px (medium), 10px (large), 14px (cards), or full (pills).

<div class="ds-demo ds-row">
  <span style="display:inline-block; width:80px; height:32px; background:var(--color-accent); border-radius:var(--radius-sm)"></span>
  <span style="display:inline-block; width:80px; height:32px; background:var(--color-accent); border-radius:var(--radius-md)"></span>
  <span style="display:inline-block; width:80px; height:32px; background:var(--color-accent); border-radius:var(--radius-lg)"></span>
  <span style="display:inline-block; width:80px; height:32px; background:var(--color-accent); border-radius:var(--radius-xl)"></span>
  <span style="display:inline-block; width:80px; height:32px; background:var(--color-accent); border-radius:var(--radius-full)"></span>
</div>

## Buttons

<div class="ds-demo ds-row">
  <a class="btn btn-primary" href="#">Watch on YouTube</a>
  <a class="btn btn-ghost" href="#">Read the article</a>
</div>

Primary is for the one main action. Ghost is for everything else. Buttons are 15px semibold with 10px corners.

## Chips, tags, and badges

<div class="ds-demo">
  <p class="ds-row" style="margin:0 0 12px"><span class="chip active">All</span><span class="chip">MikroTik</span><span class="chip">OpenWrt</span><span class="chip">VPN</span></p>
  <p class="ds-row" style="margin:0 0 12px"><span class="tag">MikroTik</span><span class="tag">RouterOS 7.25</span></p>
  <p class="ds-row" style="margin:0"><span class="badge badge-success">Passed</span><span class="badge badge-warning">Beta</span><span class="badge badge-error">Failed</span><span class="badge badge-info">Note</span></p>
</div>

Chips filter content. Tags label a post's topics. Badges show a status — success, warning, error, or info.

## Cards

<div class="ds-demo">
  <div class="card-grid" style="padding-bottom:0; grid-template-columns: repeat(2, 1fr)">
    <article class="card">
      <a class="card-thumb" href="#"><img src="/assets/images/mikrotik-reverse-proxy-netadminhub.com_.webp" alt="MikroTik Reverse Proxy"></a>
      <div class="card-body">
        <div class="card-meta"><span class="tag">MikroTik</span><span>1 Sep 2026</span></div>
        <h3 class="card-title"><a href="#">MikroTik Reverse Proxy: Host Multiple Services on One Public IP</a></h3>
        <p class="card-desc">RouterOS now includes a built-in Reverse Proxy. Publish three web applications with different domains over HTTPS using a single public IP address.</p>
        <div class="card-foot"><span>24 min</span><a class="card-link" href="#">Read →</a></div>
      </div>
    </article>
  </div>
</div>

Cards are the home page. One image (16:9), one tag, one title, a three-line description, and a footer with reading time. On hover the card lifts 3px and the border brightens.

## Pagination

The home page shows 12 posts per page. Page 1 is `/`, later pages are `/page/2/`, `/page/3/`, and so on. The footer stays reachable on every page, no matter how many posts the site grows to.

<div class="ds-demo">
  <nav class="pagination" style="padding:0">
    <a class="page-link" href="#">← Previous</a>
    <a class="page-link" href="#">1</a>
    <span class="page-link current" aria-current="page">2</span>
    <a class="page-link" href="#">3</a>
    <a class="page-link" href="#">Next →</a>
  </nav>
</div>

The current page is the accent-filled number. When a category filter or search is active, the grid shows matching posts from the whole site (via a generated `posts.json` index) and the pagination hides until the filter is cleared.

## Callouts

Use callouts for notes, tips, and warnings inside articles. Quotes stay as blockquotes; callouts are for things the reader must not miss.

<div class="callout callout-note"><span class="callout-title">Note</span><p>This is a note. Use it for extra context that does not fit the main flow.</p></div>

<div class="callout callout-tip"><span class="callout-title">Tip</span><p>This is a tip. Use it for a shortcut or a better way to do the step above.</p></div>

<div class="callout callout-warning"><span class="callout-title">Warning</span><p>This is a warning. Use it when a step can lock you out or break the setup.</p></div>

<div class="callout callout-danger"><span class="callout-title">Danger</span><p>This is a danger callout. Use it only when data loss or a security risk is involved.</p></div>

## Code and keyboard keys

Inline code looks like `/ip/firewall/nat`. A code block looks like this:

```
/interface/bridge
add name=bridge-containers
```

Press <kbd>Ctrl</kbd> + <kbd>C</kbd> to copy. Keyboard keys use the `kbd` element.

## Copy buttons

Every code block on the site gets a Copy button at its top-right corner, added by JavaScript. Clicking it copies the block and briefly shows "Copied!" in green. The button stays fixed while long lines scroll — try it on this block:

```
/ip/firewall/nat
add chain=srcnat action=masquerade out-interface=ether1
```

Inline values readers need to copy — wallet addresses on the Donate page — use `code.copyable` and get a small Copy button right after them: <code class="copyable">YOUR-WALLET-ADDRESS</code>

Classes: `.code-wrap` (positions the button against the visible block), `.copy-btn`, `.copy-btn-inline`, `code.copyable`. The clipboard API is used, with a textarea fallback for older browsers.

## Tables

| Feature | Action | Benefit |
| --- | --- | --- |
| AdList | URL import | Automatic updates every 4 hours |
| DNS cache | Increase to 20 MiB | Prevents import errors |
| Whitelist | Static DNS forward | Fixes broken websites |

## Forms

<div class="ds-demo">
  <div class="field"><label for="ds-name">Name</label><input class="input" id="ds-name" type="text" placeholder="Your name" disabled></div>
  <div class="field"><label for="ds-msg">Message</label><textarea class="textarea" id="ds-msg" placeholder="Your message" disabled></textarea></div>
  <p style="margin:0; color:var(--color-text-muted); font-size:14px">Inputs use the surface background, a 1px border, and 10px corners. Focus shows the accent ring.</p>
</div>

## Motion and focus

Motion is minimal: cards lift in 0.15s, nothing else animates. Every link, button, and input shows a visible focus ring when navigated by keyboard — try tabbing through this page. Selection uses the accent color.

## Do's and don'ts

- **Do** use a token for every color, size, space, and radius.
- **Do** keep the visual language flat and quiet. The article is the product.
- **Do** check every change at 640px and 900px widths.
- **Don't** add a new color without a token and a name.
- **Don't** add animation for its own sake.
- **Don't** use a component from another design system. This system is small on purpose.
