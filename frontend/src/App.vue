<script setup lang="ts">
const milestones = [
  { name: '工程基线', status: '已初始化' },
  { name: '小说与章节管理', status: '待开发' },
  { name: '独立审稿工作流', status: '待开发' },
  { name: '长篇记忆系统', status: '待开发' },
]
</script>

<template>
  <main class="shell">
    <header>
      <p class="eyebrow">AI WRITING · EDITORIAL QUALITY CONTROL</p>
      <h1>AI Novel Studio</h1>
      <p class="intro">从故事构思、章节创作，到独立审稿与版本质量控制。</p>
    </header>
    <section class="panel" aria-labelledby="milestone-title">
      <h2 id="milestone-title">开发里程碑</h2>
      <ul>
        <li v-for="item in milestones" :key="item.name">
          <span>{{ item.name }}</span><small>{{ item.status }}</small>
        </li>
      </ul>
    </section>
    <footer>工程初始化阶段 · 0.1.0</footer>
  </main>
</template>

<style>
:root { font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color: #e5e7eb; background: #0b1020; font-synthesis: none; }
* { box-sizing: border-box; }
body { margin: 0; min-width: 320px; min-height: 100vh; }
.shell { width: min(880px, calc(100% - 40px)); margin: 0 auto; padding: 12vh 0 48px; }
.eyebrow { color: #818cf8; font-size: 12px; font-weight: 700; letter-spacing: .16em; }
h1 { margin: 18px 0 12px; font-size: clamp(36px, 7vw, 64px); letter-spacing: -.045em; }
.intro { color: #9ca3af; font-size: 17px; line-height: 1.7; }
.panel { margin-top: 56px; padding: 28px; border: 1px solid #293247; border-radius: 18px; background: #111827; }
h2 { margin: 0 0 20px; font-size: 18px; }
ul { margin: 0; padding: 0; list-style: none; }
li { display: flex; justify-content: space-between; gap: 16px; padding: 16px 0; border-top: 1px solid #293247; }
small, footer { color: #9ca3af; }
footer { margin-top: 28px; font-size: 13px; }
</style>
