import os
import xml.etree.ElementTree as ET

def star_path(cx, cy, r):
    """Generates a 4-point celestial star with concave curved rays."""
    return (
        f"M {cx:.2f} {cy-r:.2f} "
        f"Q {cx:.2f} {cy:.2f} {cx+r:.2f} {cy:.2f} "
        f"Q {cx:.2f} {cy:.2f} {cx:.2f} {cy+r:.2f} "
        f"Q {cx:.2f} {cy:.2f} {cx-r:.2f} {cy:.2f} "
        f"Q {cx:.2f} {cy:.2f} {cx:.2f} {cy-r:.2f} Z"
    )

def diamond_path(cx, cy, r):
    """Generates a diamond path."""
    return f"M {cx:.2f} {cy-r:.2f} L {cx+r:.2f} {cy:.2f} L {cx:.2f} {cy+r:.2f} L {cx-r:.2f} {cy:.2f} Z"

# ---------------------------------------------------------------------------
# 1. banner.svg (850x240)
# ---------------------------------------------------------------------------
def generate_banner():
    stars = [
        (575, 48, 7.5, "star-twinkle-1", "#c4b5fd"),
        (610, 195, 6.0, "star-twinkle-2", "#8b5cf6"),
        (795, 55, 8.0, "star-twinkle-3", "#c4b5fd"),
        (815, 175, 6.5, "star-twinkle-1", "#a855f7"),
        (650, 218, 5.0, "star-twinkle-2", "#c4b5fd"),
        (745, 26, 6.0, "star-twinkle-3", "#8b5cf6"),
        (770, 208, 5.5, "star-twinkle-1", "#e2e8f0"),
        (535, 135, 4.5, "star-twinkle-2", "#a855f7"),
        (480, 75, 3.5, "star-twinkle-3", "#94a3b8"),
        (510, 205, 3.0, "star-twinkle-1", "#8b5cf6"),
        (825, 105, 4.0, "star-twinkle-2", "#c4b5fd"),
        (675, 35, 3.5, "star-twinkle-3", "#c4b5fd"),
    ]
    
    star_elements = []
    for cx, cy, r, cls, fill in stars:
        p = star_path(cx, cy, r)
        star_elements.append(
            f'    <path d="{p}" fill="{fill}" class="{cls}" style="transform-origin: {cx:.1f}px {cy:.1f}px;" />'
        )
    stars_xml = "\n".join(star_elements)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 240" width="850" height="240">
  <defs>
    <!-- Soft celestial corona glow filter -->
    <filter id="corona-glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="12" result="blur1" />
      <feGaussianBlur stdDeviation="4" result="blur2" />
      <feMerge>
        <feMergeNode in="blur1" />
        <feMergeNode in="blur2" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>

    <!-- Diamond bead flare glow filter -->
    <filter id="flare-glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="6" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>

    <!-- Canvas background gradient: Obsidian to deep void -->
    <linearGradient id="bg-canvas" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#09080d" />
      <stop offset="55%" stop-color="#0b0914" />
      <stop offset="100%" stop-color="#0f0c1a" />
    </linearGradient>

    <!-- Ambient nebulae -->
    <radialGradient id="nebula-purple" cx="80%" cy="40%" r="55%">
      <stop offset="0%" stop-color="#8b5cf6" stop-opacity="0.16" />
      <stop offset="50%" stop-color="#a855f7" stop-opacity="0.08" />
      <stop offset="100%" stop-color="#09080d" stop-opacity="0" />
    </radialGradient>
    <radialGradient id="nebula-dusk" cx="20%" cy="85%" r="50%">
      <stop offset="0%" stop-color="#a855f7" stop-opacity="0.08" />
      <stop offset="100%" stop-color="#09080d" stop-opacity="0" />
    </radialGradient>

    <!-- Corona ring gradient around the eclipse -->
    <radialGradient id="corona-ring" cx="44%" cy="42%" r="52%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="1" />
      <stop offset="18%" stop-color="#c4b5fd" stop-opacity="0.95" />
      <stop offset="42%" stop-color="#8b5cf6" stop-opacity="0.85" />
      <stop offset="70%" stop-color="#a855f7" stop-opacity="0.5" />
      <stop offset="100%" stop-color="#a855f7" stop-opacity="0" />
    </radialGradient>

    <!-- Moon surface gradient -->
    <linearGradient id="moon-surface" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0a0812" />
      <stop offset="60%" stop-color="#09080d" />
      <stop offset="100%" stop-color="#07060a" />
    </linearGradient>

    <!-- Border highlight gradient -->
    <linearGradient id="border-glow" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#26203a" />
      <stop offset="50%" stop-color="#3d3261" />
      <stop offset="100%" stop-color="#26203a" />
    </linearGradient>
  </defs>

  <style>
    .font-mono {{ font-family: 'Consolas', 'JetBrains Mono', monospace; }}
    .font-serif {{ font-family: 'Georgia', serif; }}
    .font-sans {{ font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif; }}

    /* Twinkling star keyframe animations */
    @keyframes twinkle {{
      0%, 100% {{ opacity: 0.25; transform: scale(0.85); }}
      50% {{ opacity: 1; transform: scale(1.15); }}
    }}
    @keyframes twinkle-alt {{
      0%, 100% {{ opacity: 0.95; transform: scale(1.12); }}
      50% {{ opacity: 0.2; transform: scale(0.82); }}
    }}
    @keyframes twinkle-slow {{
      0%, 100% {{ opacity: 0.35; transform: scale(0.9); }}
      50% {{ opacity: 1; transform: scale(1.22); }}
    }}
    .star-twinkle-1 {{ animation: twinkle 3.2s ease-in-out infinite; }}
    .star-twinkle-2 {{ animation: twinkle-alt 4.1s ease-in-out infinite; }}
    .star-twinkle-3 {{ animation: twinkle-slow 2.7s ease-in-out infinite; }}

    /* Terminal cursor blink */
    @keyframes blink {{
      0%, 49.9% {{ opacity: 1; }}
      50%, 100% {{ opacity: 0; }}
    }}
    .cursor {{ animation: blink 1.05s steps(1) infinite; }}

    /* Corona breathing */
    @keyframes corona-pulse {{
      0%, 100% {{ opacity: 0.78; }}
      50% {{ opacity: 0.96; }}
    }}
    .corona {{ animation: corona-pulse 4.8s ease-in-out infinite; }}
  </style>

  <!-- Outer canvas card with 1px border -->
  <rect x="0.5" y="0.5" width="849" height="239" rx="8" fill="url(#bg-canvas)" stroke="url(#border-glow)" stroke-width="1" />

  <!-- Ambient nebulae -->
  <rect x="0" y="0" width="850" height="240" rx="8" fill="url(#nebula-purple)" />
  <rect x="0" y="0" width="850" height="240" rx="8" fill="url(#nebula-dusk)" />

  <!-- Celestial grid background stars -->
  <g fill="#3d3261" opacity="0.35">
    <circle cx="510" cy="50" r="1" />
    <circle cx="550" cy="90" r="1" />
    <circle cx="630" cy="40" r="1" />
    <circle cx="780" cy="110" r="1" />
    <circle cx="820" cy="70" r="1" />
    <circle cx="560" cy="210" r="1" />
    <circle cx="680" cy="230" r="1" />
    <circle cx="790" cy="190" r="1" />
  </g>

  <!-- RIGHT SIDE ARTWORK: LUNAR / SOLAR ECLIPSE -->
  <g id="eclipse-artwork">
    <!-- Orbital arcs -->
    <ellipse cx="696" cy="120" rx="104" ry="46" transform="rotate(-22 696 120)" fill="none" stroke="#8b5cf6" stroke-opacity="0.28" stroke-width="1" stroke-dasharray="4 7" />
    <ellipse cx="696" cy="120" rx="142" ry="62" transform="rotate(-12 696 120)" fill="none" stroke="#c4b5fd" stroke-opacity="0.16" stroke-width="1" stroke-dasharray="6 12" />
    <ellipse cx="696" cy="120" rx="74" ry="32" transform="rotate(-32 696 120)" fill="none" stroke="#a855f7" stroke-opacity="0.24" stroke-width="1" stroke-dasharray="2 5" />

    <!-- Orbital satellite points -->
    <circle cx="598" cy="98" r="2.2" fill="#c4b5fd" />
    <circle cx="786" cy="148" r="2.5" fill="#8b5cf6" />
    <circle cx="738" cy="62" r="1.6" fill="#a855f7" />
    <circle cx="638" cy="154" r="1.8" fill="#e2e8f0" />

    <!-- Radiant Corona Outer Glow (Behind Moon) -->
    <circle cx="690" cy="115" r="64" fill="url(#corona-ring)" filter="url(#corona-glow)" class="corona" />
    <circle cx="690" cy="115" r="56" fill="url(#corona-ring)" opacity="0.9" />

    <!-- Moon Body (Dark overlapping disc) -->
    <circle cx="698" cy="122" r="49" fill="url(#moon-surface)" />
    <!-- Secondary shadow contour -->
    <circle cx="701" cy="124" r="48" fill="#08070d" opacity="0.95" />

    <!-- Crescent Rim Highlight along upper-left crest -->
    <path d="M 655 92 A 49 49 0 0 1 716 74" fill="none" stroke="#c4b5fd" stroke-width="1.8" stroke-linecap="round" opacity="0.85" />

    <!-- Diamond Ring / Solar Flare Bead at rim -->
    <g transform="translate(654, 86)">
      <circle cx="0" cy="0" r="5" fill="#ffffff" filter="url(#flare-glow)" />
      <circle cx="0" cy="0" r="2.5" fill="#ffffff" />
      <path d="{star_path(0, 0, 16)}" fill="#ffffff" filter="url(#flare-glow)" opacity="0.9" />
      <line x1="-20" y1="0" x2="20" y2="0" stroke="#ffffff" stroke-width="0.8" stroke-opacity="0.75" />
      <line x1="0" y1="-20" x2="0" y2="20" stroke="#ffffff" stroke-width="0.8" stroke-opacity="0.75" />
    </g>

    <!-- Twinkling 4-point stars around eclipse -->
{stars_xml}
  </g>

  <!-- LEFT SIDE TYPOGRAPHY & UI -->
  <g id="hero-content">
    <!-- Top eyebrow badge pill -->
    <rect x="46" y="36" width="258" height="24" rx="12" fill="#13101e" stroke="#26203a" stroke-width="1" />
    <path d="{star_path(58, 48, 4.5)}" fill="#8b5cf6" />
    <text x="72" y="52.5" class="font-mono" font-size="9.5" font-weight="700" fill="#c4b5fd" letter-spacing="1.5">PHASE 01 // CELESTIAL ARCHITECTURE</text>

    <!-- Main display title: CALY -->
    <text x="46" y="112" class="font-serif" font-size="46" font-weight="700" fill="#f3e8ff" letter-spacing="6">CALY</text>
    <!-- Celestial decorative flourish next to title -->
    <path d="{star_path(230, 96, 7)}" fill="#8b5cf6" opacity="0.85" />
    <path d="{diamond_path(248, 96, 3.5)}" fill="#a855f7" opacity="0.65" />

    <!-- Subtitle: Systems Developer & Domain -->
    <text x="47" y="145" class="font-sans" font-size="12.5" font-weight="600" fill="#c4b5fd" letter-spacing="2">SYSTEMS DEVELOPER  •  RUST &amp; EMBEDDED</text>

    <!-- Terminal line container -->
    <rect x="46" y="168" width="446" height="36" rx="6" fill="#13101e" stroke="#26203a" stroke-width="1" />
    
    <!-- Terminal line prompt & text -->
    <text x="58" y="191" class="font-mono" font-size="11.5" letter-spacing="0.3">
      <tspan fill="#8b5cf6" font-weight="700">&gt; </tspan>
      <tspan fill="#94a3b8">crafting low-level audio, video, and hardware systems</tspan>
    </text>
    
    <!-- Animated blinking block cursor -->
    <rect x="452" y="179" width="7" height="15" rx="1" fill="#a855f7" class="cursor" />
  </g>
</svg>"""
    return svg

# ---------------------------------------------------------------------------
# 2. divider.svg (850x44)
# ---------------------------------------------------------------------------
def generate_divider():
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 44" width="850" height="44">
  <defs>
    <!-- Fading gradient lines from transparent to purple -->
    <linearGradient id="div-fade-left" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#26203a" stop-opacity="0" />
      <stop offset="50%" stop-color="#26203a" stop-opacity="0.8" />
      <stop offset="85%" stop-color="#3d3261" stop-opacity="1" />
      <stop offset="100%" stop-color="#8b5cf6" stop-opacity="1" />
    </linearGradient>
    <linearGradient id="div-fade-right" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#8b5cf6" stop-opacity="1" />
      <stop offset="15%" stop-color="#3d3261" stop-opacity="1" />
      <stop offset="50%" stop-color="#26203a" stop-opacity="0.8" />
      <stop offset="100%" stop-color="#26203a" stop-opacity="0" />
    </linearGradient>
  </defs>

  <style>
    .font-mono {{ font-family: 'Consolas', 'JetBrains Mono', monospace; }}
  </style>

  <!-- Left fading rule -->
  <line x1="30" y1="22" x2="256" y2="22" stroke="url(#div-fade-left)" stroke-width="1.2" />

  <!-- Left constellation emblem -->
  <path d="{diamond_path(268, 22, 3)}" fill="#8b5cf6" />
  <path d="{star_path(288, 22, 5.5)}" fill="#c4b5fd" />
  <path d="{diamond_path(304, 22, 2)}" fill="#a855f7" />

  <!-- Center typography -->
  <text x="425" y="26" text-anchor="middle" class="font-mono" font-size="10.5" font-weight="700" fill="#c4b5fd" letter-spacing="3">FEATURED CONSTELLATIONS</text>

  <!-- Top and bottom celestial accents -->
  <path d="{diamond_path(425, 9, 2.2)}" fill="#8b5cf6" opacity="0.75" />
  <path d="{diamond_path(425, 35, 2.2)}" fill="#8b5cf6" opacity="0.75" />

  <!-- Right constellation emblem -->
  <path d="{diamond_path(546, 22, 2)}" fill="#a855f7" />
  <path d="{star_path(562, 22, 5.5)}" fill="#c4b5fd" />
  <path d="{diamond_path(582, 22, 3)}" fill="#8b5cf6" />

  <!-- Right fading rule -->
  <line x1="594" y1="22" x2="820" y2="22" stroke="url(#div-fade-right)" stroke-width="1.2" />
</svg>"""
    return svg

# ---------------------------------------------------------------------------
# 3. projects-grid.svg (850x230)
# ---------------------------------------------------------------------------
def generate_projects_grid():
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 230" width="850" height="230">
  <defs>
    <!-- Card surface gradients -->
    <linearGradient id="card-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#141122" />
      <stop offset="100%" stop-color="#110e1a" />
    </linearGradient>

    <!-- Top highlight lines -->
    <linearGradient id="top-glow-left" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#26203a" stop-opacity="0.2" />
      <stop offset="40%" stop-color="#a855f7" stop-opacity="0.8" />
      <stop offset="100%" stop-color="#26203a" stop-opacity="0.2" />
    </linearGradient>
    <linearGradient id="top-glow-right" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#26203a" stop-opacity="0.2" />
      <stop offset="40%" stop-color="#8b5cf6" stop-opacity="0.8" />
      <stop offset="100%" stop-color="#26203a" stop-opacity="0.2" />
    </linearGradient>
  </defs>

  <style>
    .font-mono {{ font-family: 'Consolas', 'JetBrains Mono', monospace; }}
    .font-serif {{ font-family: 'Georgia', serif; }}
    .font-sans {{ font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif; }}

    /* Pulsing status aura */
    @keyframes pulse-aura {{
      0%, 100% {{ opacity: 0.85; transform: scale(1); }}
      50% {{ opacity: 0.15; transform: scale(2.3); }}
    }}
    .pulse-purple {{
      transform-origin: 36px 197px;
      animation: pulse-aura 2.4s ease-in-out infinite;
    }}
    .pulse-violet {{
      transform-origin: 471px 197px;
      animation: pulse-aura 2.4s ease-in-out infinite 0.6s;
    }}
  </style>

  <!-- ==================== LEFT CARD: ECLIPSE ==================== -->
  <g id="card-eclipse">
    <!-- Card Surface (414x229) with 1px border -->
    <rect x="0.5" y="0.5" width="414" height="229" rx="8" fill="url(#card-bg)" stroke="#26203a" stroke-width="1" />
    <!-- 1px Top Glow Highlight -->
    <line x1="20" y1="1" x2="394" y2="1" stroke="url(#top-glow-left)" stroke-width="1.2" />

    <!-- Subtle watermark background arc -->
    <path d="M 330 30 A 80 80 0 0 1 400 130" fill="none" stroke="#8b5cf6" stroke-opacity="0.08" stroke-width="1" stroke-dasharray="3 6" />

    <!-- Vector Icon Badge Container -->
    <rect x="24" y="24" width="44" height="44" rx="8" fill="#1b162b" stroke="#3d3261" stroke-width="1" />
    
    <!-- Vector Logo: Crescent / Eclipsed Moon + Sharp 4-point Star -->
    <g transform="translate(24, 24)">
      <!-- Crescent moon vector -->
      <path d="M 22 10 A 11 11 0 1 0 33 22 A 8.8 8.8 0 1 1 22 10 Z" fill="#c4b5fd" />
      <!-- Sharp 4-point star in crest opening -->
      <path d="{star_path(29, 14, 5.5)}" fill="#a855f7" />
    </g>

    <!-- Card Title -->
    <text x="80" y="44" class="font-serif" font-size="20" font-weight="700" fill="#f3e8ff" letter-spacing="2.2">ECLIPSE</text>

    <!-- Tech Tag Pill: RUST / EGUI -->
    <rect x="80" y="52" width="94" height="19" rx="4" fill="#1d1633" stroke="#3d3261" stroke-width="1" />
    <text x="127" y="65" text-anchor="middle" class="font-mono" font-size="9" font-weight="700" fill="#c4b5fd" letter-spacing="0.8">RUST / EGUI</text>

    <!-- Description (3 clean lines) -->
    <text x="24" y="106" class="font-sans" font-size="12" fill="#94a3b8" letter-spacing="0.1">Cross-platform desktop music player with lossless</text>
    <text x="24" y="126" class="font-sans" font-size="12" fill="#94a3b8" letter-spacing="0.1">multi-format audio extraction, synchronized lyrics,</text>
    <text x="24" y="146" class="font-sans" font-size="12" fill="#94a3b8" letter-spacing="0.1">and custom dark themes.</text>

    <!-- Bottom Status Line Separator -->
    <line x1="24" y1="173" x2="390" y2="173" stroke="#221c33" stroke-width="1" />

    <!-- Status Indicator: Animated pulsing purple dot -->
    <circle cx="36" cy="197" r="4" fill="#a855f7" class="pulse-purple" />
    <circle cx="36" cy="197" r="3.2" fill="#a855f7" />

    <!-- Status text -->
    <text x="50" y="201" class="font-mono" font-size="10" font-weight="700" fill="#c4b5fd" letter-spacing="1.4">ACTIVE DEVELOPMENT</text>

    <!-- Right side decorative star -->
    <path d="{star_path(382, 197, 4)}" fill="#8b5cf6" opacity="0.7" />
  </g>

  <!-- ==================== RIGHT CARD: VESPER ==================== -->
  <g id="card-vesper">
    <!-- Card Surface (414x229) with 1px border -->
    <rect x="435.5" y="0.5" width="414" height="229" rx="8" fill="url(#card-bg)" stroke="#26203a" stroke-width="1" />
    <!-- 1px Top Glow Highlight -->
    <line x1="455" y1="1" x2="829" y2="1" stroke="url(#top-glow-right)" stroke-width="1.2" />

    <!-- Subtle watermark background arc -->
    <path d="M 765 30 A 80 80 0 0 1 835 130" fill="none" stroke="#c4b5fd" stroke-opacity="0.08" stroke-width="1" stroke-dasharray="3 6" />

    <!-- Vector Icon Badge Container -->
    <rect x="459" y="24" width="44" height="44" rx="8" fill="#1b162b" stroke="#3d3261" stroke-width="1" />

    <!-- Vector Logo: Evening Star with outer rays inside minimal frame -->
    <g transform="translate(459, 24)">
      <!-- Outer diamond frame -->
      <rect x="8" y="8" width="28" height="28" rx="4" fill="none" stroke="#3d3261" stroke-width="1" stroke-dasharray="2 3" />
      <!-- Secondary 45-degree ray star -->
      <path d="{diamond_path(22, 22, 7.5)}" fill="#8b5cf6" opacity="0.85" />
      <!-- Primary 4-point evening star -->
      <path d="{star_path(22, 22, 11)}" fill="#c4b5fd" />
      <!-- Center starlight core -->
      <circle cx="22" cy="22" r="1.8" fill="#ffffff" />
    </g>

    <!-- Card Title -->
    <text x="515" y="44" class="font-serif" font-size="20" font-weight="700" fill="#f3e8ff" letter-spacing="2.2">VESPER</text>

    <!-- Tech Tag Pill: RUST / LIBMPV -->
    <rect x="515" y="52" width="108" height="19" rx="4" fill="#1d1633" stroke="#3d3261" stroke-width="1" />
    <text x="569" y="65" text-anchor="middle" class="font-mono" font-size="9" font-weight="700" fill="#c4b5fd" letter-spacing="0.8">RUST / LIBMPV</text>

    <!-- Description (3 clean lines) -->
    <text x="459" y="106" class="font-sans" font-size="12" fill="#94a3b8" letter-spacing="0.1">Lightweight native Windows media player,</text>
    <text x="459" y="126" class="font-sans" font-size="12" fill="#94a3b8" letter-spacing="0.1">subtitle extractor, and custom hybrid video</text>
    <text x="459" y="146" class="font-sans" font-size="12" fill="#94a3b8" letter-spacing="0.1">codec pipeline.</text>

    <!-- Bottom Status Line Separator -->
    <line x1="459" y1="173" x2="825" y2="173" stroke="#221c33" stroke-width="1" />

    <!-- Status Indicator: Animated pulsing violet dot -->
    <circle cx="471" cy="197" r="4" fill="#8b5cf6" class="pulse-violet" />
    <circle cx="471" cy="197" r="3.2" fill="#8b5cf6" />

    <!-- Status text -->
    <text x="485" y="201" class="font-mono" font-size="10" font-weight="700" fill="#c4b5fd" letter-spacing="1.4">ACTIVE DEVELOPMENT</text>

    <!-- Right side decorative star -->
    <path d="{star_path(817, 197, 4)}" fill="#a855f7" opacity="0.7" />
  </g>
</svg>"""
    return svg

# ---------------------------------------------------------------------------
# 4. btn-eclipse.svg (240x40)
# ---------------------------------------------------------------------------
def generate_btn_eclipse():
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 40" width="240" height="40">
  <defs>
    <linearGradient id="btn-bg-eclipse" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#181427" />
      <stop offset="100%" stop-color="#110e1a" />
    </linearGradient>
  </defs>

  <style>
    .font-mono {{ font-family: 'Consolas', 'JetBrains Mono', monospace; }}
  </style>

  <!-- Button Card Surface (240x40) -->
  <rect x="1" y="1" width="238" height="38" rx="5" fill="url(#btn-bg-eclipse)" stroke="#3d3261" stroke-width="1" />

  <!-- Subtle Top Highlight Line -->
  <line x1="8" y1="2" x2="232" y2="2" stroke="#8b5cf6" stroke-opacity="0.35" stroke-width="1" />

  <!-- Left Mini Vector Icon: Crescent Moon (#a855f7) -->
  <path d="M 28 14.5 A 5.5 5.5 0 1 0 33.5 20 A 4.3 4.3 0 1 1 28 14.5 Z" fill="#a855f7" />

  <!-- Label Text -->
  <text x="42" y="24" class="font-mono" font-size="11" font-weight="700" fill="#e2e8f0" letter-spacing="1.5">ECLIPSE REPOSITORY</text>

  <!-- Right Mini Vector Icon: Diagonal External Link Arrow (#c4b5fd) -->
  <path d="M 197 23 L 204 16 M 199 16 L 204 16 L 204 21" fill="none" stroke="#c4b5fd" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" />
</svg>"""
    return svg

# ---------------------------------------------------------------------------
# 5. btn-vesper.svg (240x40)
# ---------------------------------------------------------------------------
def generate_btn_vesper():
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 40" width="240" height="40">
  <defs>
    <linearGradient id="btn-bg-vesper" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#181427" />
      <stop offset="100%" stop-color="#110e1a" />
    </linearGradient>
  </defs>

  <style>
    .font-mono {{ font-family: 'Consolas', 'JetBrains Mono', monospace; }}
  </style>

  <!-- Button Card Surface (240x40) -->
  <rect x="1" y="1" width="238" height="38" rx="5" fill="url(#btn-bg-vesper)" stroke="#3d3261" stroke-width="1" />

  <!-- Subtle Top Highlight Line -->
  <line x1="8" y1="2" x2="232" y2="2" stroke="#8b5cf6" stroke-opacity="0.35" stroke-width="1" />

  <!-- Left Mini Vector Icon: Small 4-Point Star (#c4b5fd) -->
  <path d="{star_path(30, 20, 5.5)}" fill="#c4b5fd" />

  <!-- Label Text -->
  <text x="45" y="24" class="font-mono" font-size="11" font-weight="700" fill="#e2e8f0" letter-spacing="1.5">VESPER REPOSITORY</text>

  <!-- Right Mini Vector Icon: Diagonal External Link Arrow (#c4b5fd) -->
  <path d="M 195 23 L 202 16 M 197 16 L 202 16 L 202 21" fill="none" stroke="#c4b5fd" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" />
</svg>"""
    return svg

# ---------------------------------------------------------------------------
# 6. stack-footer.svg (850x110)
# ---------------------------------------------------------------------------
def generate_stack_footer():
    pills = [
        {"x": 24, "w": 108, "label": "RUST", "type": "rust", "ix": 55, "lx": 69},
        {"x": 152, "w": 114, "label": "C / C++", "type": "c", "ix": 178, "lx": 192},
        {"x": 286, "w": 142, "label": "ESP32 / IOT", "type": "esp32", "ix": 312, "lx": 326},
        {"x": 448, "w": 118, "label": "FFMPEG", "type": "ffmpeg", "ix": 478, "lx": 492},
        {"x": 586, "w": 110, "label": "WIN32", "type": "win32", "ix": 618, "lx": 632},
        {"x": 716, "w": 110, "label": "LINUX", "type": "linux", "ix": 748, "lx": 762},
    ]
    
    sep_xs = [142, 276, 438, 576, 706]
    separators = []
    for sx in sep_xs:
        p = star_path(sx, 73, 3.5)
        separators.append(f'  <path d="{p}" fill="#8b5cf6" opacity="0.6" />')
    separators_xml = "\n".join(separators)

    pill_elements = []
    for p in pills:
        px = p["x"]
        pw = p["w"]
        lbl = p["label"]
        ptype = p["type"]
        ix = p["ix"]
        lx = p["lx"]
        iy = 73
        
        rect = f'<rect x="{px}" y="56" width="{pw}" height="34" rx="6" fill="#171325" stroke="#2d2449" stroke-width="1" />'
        
        if ptype == "rust":
            icon = f'<path d="{star_path(ix, iy, 6)}" fill="#8b5cf6" /><circle cx="{ix}" cy="{iy}" r="2" fill="#171325" />'
        elif ptype == "c":
            icon = f'<path d="M {ix-3} {iy-4} L {ix-6} {iy} L {ix-3} {iy+4} M {ix+3} {iy-4} L {ix+6} {iy} L {ix+3} {iy+4}" fill="none" stroke="#a855f7" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />'
        elif ptype == "esp32":
            icon = (
                f'<rect x="{ix-5}" y="{iy-5}" width="10" height="10" rx="1.5" fill="none" stroke="#c4b5fd" stroke-width="1.2" />'
                f'<line x1="{ix-7}" y1="{iy}" x2="{ix-5}" y2="{iy}" stroke="#c4b5fd" stroke-width="1.2" />'
                f'<line x1="{ix+5}" y1="{iy}" x2="{ix+7}" y2="{iy}" stroke="#c4b5fd" stroke-width="1.2" />'
                f'<line x1="{ix}" y1="{iy-7}" x2="{ix}" y2="{iy-5}" stroke="#c4b5fd" stroke-width="1.2" />'
                f'<line x1="{ix}" y1="{iy+5}" x2="{ix}" y2="{iy+7}" stroke="#c4b5fd" stroke-width="1.2" />'
            )
        elif ptype == "ffmpeg":
            icon = f'<path d="M {ix-5} {iy-5} L {ix+4} {iy} L {ix-5} {iy+5} Z" fill="#8b5cf6" />'
        elif ptype == "win32":
            icon = (
                f'<rect x="{ix-5}" y="{iy-5}" width="4.5" height="4.5" fill="#c4b5fd" />'
                f'<rect x="{ix+1}" y="{iy-5}" width="4.5" height="4.5" fill="#c4b5fd" />'
                f'<rect x="{ix-5}" y="{iy+1}" width="4.5" height="4.5" fill="#c4b5fd" />'
                f'<rect x="{ix+1}" y="{iy+1}" width="4.5" height="4.5" fill="#c4b5fd" />'
            )
        elif ptype == "linux":
            icon = (
                f'<path d="M {ix-5} {iy-4} L {ix-1} {iy} L {ix-5} {iy+4}" fill="none" stroke="#a855f7" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />'
                f'<line x1="{ix+1}" y1="{iy+4}" x2="{ix+5}" y2="{iy+4}" stroke="#a855f7" stroke-width="1.5" stroke-linecap="round" />'
            )
        else:
            icon = f'<path d="{diamond_path(ix, iy, 4)}" fill="#8b5cf6" />'

        text = f'<text x="{lx}" y="{iy+4}" class="font-mono" font-size="10.5" font-weight="700" fill="#e2e8f0" letter-spacing="0.8">{lbl}</text>'
        
        pill_elements.append(f'  <g>\n    {rect}\n    {icon}\n    {text}\n  </g>')

    pills_xml = "\n".join(pill_elements)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 110" width="850" height="110">
  <style>
    .font-mono {{ font-family: 'Consolas', 'JetBrains Mono', monospace; }}
  </style>

  <!-- Card Surface (850x110) with 1px border -->
  <rect x="0.5" y="0.5" width="849" height="109" rx="8" fill="#13101e" stroke="#26203a" stroke-width="1" />

  <!-- Top header row -->
  <path d="{star_path(28, 25, 4.5)}" fill="#8b5cf6" />
  <text x="40" y="29" class="font-mono" font-size="10.5" font-weight="700" fill="#c4b5fd" letter-spacing="2">CORE DOMAINS &amp; ARSENAL</text>
  <text x="824" y="29" text-anchor="end" class="font-mono" font-size="9" font-weight="600" fill="#94a3b8" letter-spacing="1.5">LOW-LEVEL ARCHITECTURE</text>

  <!-- Subtle header divider rule -->
  <line x1="24" y1="42" x2="826" y2="42" stroke="#221b35" stroke-width="1" />

  <!-- 4-point star separators between pill sections -->
{separators_xml}

  <!-- Stack badges -->
{pills_xml}
</svg>"""
    return svg

# ---------------------------------------------------------------------------
# 7. README.md
# ---------------------------------------------------------------------------
def generate_readme():
    return """<p align="center">
  <img src="./assets/banner.svg" alt="Caly // Lunar Eclipse &amp; Vesper Systems Developer Banner" width="100%" />
</p>

<p align="center">
  <img src="./assets/divider.svg" alt="Section Divider: Featured Constellations" width="100%" />
</p>

<p align="center">
  <img src="./assets/projects-grid.svg" alt="Featured Constellations: Eclipse &amp; Vesper" width="100%" />
</p>

<p align="center">
  <a href="https://github.com/Caly-sys/Eclipse">
    <img src="./assets/btn-eclipse.svg" alt="Eclipse Repository" height="40" />
  </a>
  &nbsp;&nbsp;&nbsp;
  <a href="https://github.com/Caly-sys/vesper">
    <img src="./assets/btn-vesper.svg" alt="Vesper Repository" height="40" />
  </a>
</p>

<br />

<p align="center">
  <img src="./assets/stack-footer.svg" alt="Core Domains &amp; Arsenal Stack Footer" width="100%" />
</p>

<br />

<p align="center">
  <img src="https://komarev.com/ghpvc/?username=Caly-sys&amp;color=8b5cf6&amp;style=flat-square&amp;label=OBSERVERS" alt="Telemetry: Caly Observers Count" />
</p>
"""

def main():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets_dir = os.path.join(repo_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    
    files = {
        os.path.join(assets_dir, "banner.svg"): generate_banner(),
        os.path.join(assets_dir, "divider.svg"): generate_divider(),
        os.path.join(assets_dir, "projects-grid.svg"): generate_projects_grid(),
        os.path.join(assets_dir, "btn-eclipse.svg"): generate_btn_eclipse(),
        os.path.join(assets_dir, "btn-vesper.svg"): generate_btn_vesper(),
        os.path.join(assets_dir, "stack-footer.svg"): generate_stack_footer(),
        os.path.join(repo_dir, "README.md"): generate_readme(),
    }
    
    for path, content in files.items():
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Wrote {path}")
        if path.endswith(".svg"):
            try:
                ET.fromstring(content)
                print(f"  [XML VALID] {os.path.basename(path)}")
            except ET.ParseError as e:
                print(f"  [XML ERROR] {os.path.basename(path)}: {e}")

if __name__ == "__main__":
    main()
