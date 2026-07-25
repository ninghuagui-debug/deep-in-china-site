# Deep in China 网站后期规划方案 v1.0

> 最后更新：2026-07-17 | 状态：初版，持续迭代

---

## 一、现状盘点

### 当前已完成
| 模块 | 状态 | 说明 |
|------|------|------|
| 品牌定位 | ✅ 完成 | Deep in China, slogan "Go deeper than any tourist ever goes" |
| 主页框架 | ✅ 完成 | Hero + 视频网格 + 交互地图 + About + Footer |
| 交互地图 | ✅ 完成 | GeoJSON真实省界SVG, hover/click交互, 省份详情面板 |
| 省份数据 | ✅ 完成 | 14个省份hook+description+SEO字段 (provinces.json) |
| 竞品差异化 | ✅ 完成 | 其他频道无交互地图，这是独特卖点 |
| 管线模板 | ✅ 完成 | video-pipeline/ 下3个md模板文件 |

### 当前缺失
| 模块 | 优先级 | 说明 |
|------|--------|------|
| 省份数据补全 | P0 | 还差20个省份的hook/description/SEO |
| YouTube视频嵌入 | P0 | videoIds全为空，等首批视频上线 |
| 省份详情页 | P1 | 当前只有弹窗，需要独立页面做SEO |
| 响应式优化 | P1 | 移动端适配需调整地图交互 |
| 品牌视觉资产 | P1 | Hero图片、省份封面图全部缺失 |
| SEO基础设施 | P2 | meta标签、sitemap、robots.txt |
| 域名+部署 | P2 | deepinchina.com 域名购买+海外托管 |
| 社交媒体联动 | P3 | Twitter/Instagram/Facebook账号和内容策略 |

---

## 二、网站架构演进路线

### Phase 1 — MVP上线（当前 → 首批5条视频发布）

**目标**：网站能跑、有视频、能引流

1. **补全34省数据**
   - 剩余20省的hook/description/keywords/meta字段
   - 规则：每省必须有1个反常识hook + 1组对比数据 + 5个SEO关键词
   - 敏感省份(西藏/新疆/港澳台)强制使用 "X, China" 格式
   - 执行者：WorkBuddy（数据编写）+ ClawX（hook创意审核）

2. **YouTube视频嵌入**
   - videoIds填入首批视频YouTube ID
   - 嵌入方式：iframe embed + 点击省份弹窗内播放
   - 视频网格区自动展示最新视频（按发布时间排序）
   - 无视频省份显示"Coming Soon"占位

3. **移动端适配**
   - 地图在小屏改为可滚动缩放模式
   - 视频网格从3列→1列
   - Hero区文案字体适配
   - Footer简化

4. **部署上线**
   - 域名：deepinchina.com（需购买）
   - 托管：Cloudflare Pages / Vercel / Netlify（免费层足够）
   - 部署方式：纯静态站，直接push dist文件夹
   - HTTPS：Cloudflare/Vercel自带
   - CDN：自带全球CDN，适合海外用户

**交付标准**：网站可访问、有至少5条视频可播放、34省数据完整

---

### Phase 2 — 独立省份页 + SEO强化（5-15条视频期）

**目标**：每个省份有独立SEO页面，搜索引擎可索引

1. **省份详情页模板**
   ```
   /provinces/sichuan.html    ← 每省一个独立页面
   /provinces/guizhou.html
   ...
   ```
   - 页面结构：Hero图 + 省份hook + 视频列表 + 数据卡片区 + 相关省份推荐
   - 数据卡片：面积/人口/海拔/特色数据对比（用hookData渲染）
   - 相关省份：基于地理邻近或主题关联推荐（如四川→重庆→贵州）

2. **SEO基础设施**
   - 每个省份页独立meta title/description（已有provinces.json）
   - 生成 sitemap.xml（34省 + 主页 + 约40个URL）
   - 生成 robots.txt
   - Open Graph标签（YouTube引流时社交媒体预览）
   - 结构化数据：JSON-LD（VideoObject + Place标记）

3. **主页→省份页联动**
   - 地图点击从弹窗改为跳转省份页（保留弹窗作为快速预览）
   - 视频网格卡片的"Learn More"链接到省份页
   - 省份页底部"Back to Map"返回主页

4. **面包屑导航**
   - Home > Sichuan > Videos
   - 利于SEO和用户理解当前位置

**交付标准**：34个省份页可访问、sitemap提交Google、SEO得分>80

---

### Phase 3 — 内容增长 + 社交联动（15-50条视频期）

**目标**：内容矩阵成型，社交媒体形成流量闭环

1. **频道页（Topic Pages）**
   ```
   /topics/spicy-china.html      ← 跨省份主题聚合
   /topics/silk-road.html
   /topics/extreme-china.html
   /topics/hidden-cities.html
   ```
   - 把相关省份的视频按主题聚合
   - 每个主题页有独立SEO（如 "Spicy Food in China — From Sichuan to Hunan"）
   - 主题页之间互相链接，形成内链网络

2. **社交媒体整合**
   - 每个视频页底部嵌入社交分享按钮
   - Twitter/X账号自动推送新视频（可自动化）
   - Instagram：省份精选图片（后期）
   - 社交账号链接已在site.json配置（目前为空，待注册）

3. **博客/文章区**
   ```
   /blog/sichuan-beyond-the-spice.html
   /blog/why-chongqing-breaks-every-rule.html
   ```
   - 每条视频配套1篇深度文章（2000-3000字）
   - 文章嵌入视频 + 补充文字内容
   - 长尾SEO关键词覆盖（文章比视频更容易被Google索引）
   - 执行者：ClawX六脑改写 + WorkBuddy审核

4. **邮件订阅**
   - "Get notified when we explore a new province"
   - 简单Mailchimp/ConvertKit嵌入
   - 新视频发布时邮件推送

**交付标准**：4个主题页上线、Twitter自动推送运行、博客区有10+篇文章

---

### Phase 4 — 全球复制 + 商业化（50+视频 / 流量稳定期）

**目标**：模板复制到其他国家，探索变现

1. **全球复制架构**
   ```
   deepinchina.com      ← 中国（当前）
   deepinjapan.com      ← 日本（复制模板）
   deepinindia.com      ← 印度
   deepinitaly.com      ← 意大利
   ...
   ```
   - 架构已经是模板化的（data/map/pages分离）
   - 复制流程：换site.json品牌名 → 换provinces.json数据 → 换GeoJSON地图 → 换SVG → 部署
   - 每个国家一个独立域名和品牌
   - 通用组件库：共享CSS/JS/模板，只换数据和地图

2. **变现模式**
   | 方式 | 优先级 | 预期收入 | 说明 |
   |------|--------|----------|------|
   | YouTube AdSense | P0 | 主要收入 | 视频播放量直接变现 |
   | 旅行联盟营销 | P1 | 中等 | Booking.com/Agoda住宿推荐链接 |
   | 品牌合作 | P2 | 高单额 | 旅游局/航空公司赞助内容 |
   | 付费课程/指南 | P3 | 待评估 | 深度旅行指南PDF售卖 |
   | 会员订阅 | P3 | 待评估 | Patreon/YouTube会员 |

3. **数据驱动优化**
   - Google Analytics嵌入（从Phase 1就可以加）
   - 追踪：省份页访问量 → 视频播放率 → YouTube跳转率
   - 根据数据调整：哪省内容最受欢迎 → 优先生产该省更多内容
   - A/B测试：hook文案、页面布局、CTA按钮位置

4. **技术升级（可选）**
   - 从纯静态升级到 Next.js / Astro SSG（需要时再升级）
   - 当前纯静态足以支撑Phase 1-3，流量超过10万/月再考虑
   - 好处：更好的SEO控制、动态渲染、API routes

**交付标准**：至少1个国家站点复制上线、YouTube AdSense激活、Analytics数据开始驱动决策

---

## 三、数据架构规范

### 文件结构（当前 + 后期）
```
deep-in-china-site/
├── index.html                 ← 主页（当前）
├── data/
│   ├── site.json              ← 品牌配置（当前）
│   ├── provinces.json         ← 34省数据（当前，待补全）
│   └── topics.json            ← 主题聚合数据（Phase 3新增）
│   └── blog.json              ← 博客文章索引（Phase 3新增）
├── map/
│   ├── china-geo.json         ← GeoJSON原始数据（当前）
│   ├── china-real.svg         ← 省界SVG地图（当前）
│   └── china-interactive.svg  ← 增强版地图（Phase 2，标签优化）
├── provinces/                 ← 独立省份页（Phase 2新增）
│   ├── sichuan.html
│   ├── guizhou.html
│   └── ... (34个)
├── topics/                    ← 主题页（Phase 3新增）
│   ├── spicy-china.html
│   └── ...
├── blog/                      ← 博客页（Phase 3新增）
│   ├── sichuan-beyond-spice.html
│   └── ...
├── assets/
│   ├── css/style.css          ← 样式（当前）
│   ├── js/app.js              ← 交互逻辑（当前）
│   ├── js/province.js         ← 省份页逻辑（Phase 2新增）
│   ├── images/                ← 图片资产（Phase 1新增）
│   │   ├── hero-mountains.jpg
│   │   ├── hero-city.jpg
│   │   ├── province-covers/   ← 每省封面图
│   │   └── og-images/         ← 社交分享预览图
│   └── fonts/                 ← 品牌字体（Phase 2可选）
├── seo/
│   ├── sitemap.xml            ← Phase 2生成
│   └── robots.txt             ← Phase 2生成
└── templates/                 ← 页面模板（Phase 2，供批量生成用）
    ├── province-template.html
    ├── topic-template.html
    └── blog-template.html
```

### provinces.json 数据规范
每个省份必须包含以下字段：
```json
{
  "id": "sichuan",              // slug，URL路径用
  "nameEn": "Sichuan",          // 英文名（敏感省份加 ", China"）
  "nameZh": "四川",              // 中文名（内部标识用）
  "slug": "sichuan",             // URL slug
  "hook": "...",                 // 反常识一句话hook
  "hookData": "...",             // hook的数据支撑
  "description": "...",          // 3-5行省份描述
  "videoIds": ["yt_id_1"],      // YouTube视频ID列表
  "keywords": [...],             // 5个SEO关键词
  "metaTitle": "...",            // SEO meta title (<60字符)
  "metaDescription": "...",      // SEO meta description (<160字符)
  "coverImage": "",              // 省份封面图路径（Phase 1新增）
  "dataCards": [                 // 数据对比卡片（Phase 2新增）
    {"label": "Area", "value": "486,000 km²", "compare": "Larger than California"},
    {"label": "Population", "value": "83M", "compare": "More than Germany"}
  ],
  "relatedProvinces": ["chongqing", "guizhou"]  // 关联省份（Phase 2新增）
}
```

### 新增数据文件规范

**topics.json** (Phase 3):
```json
[
  {
    "id": "spicy-china",
    "title": "Spicy China — From Sichuan to Hunan",
    "slug": "spicy-china",
    "description": "...",
    "provinces": ["sichuan", "hunan", "guizhou"],
    "keywords": [...],
    "metaTitle": "...",
    "metaDescription": "..."
  }
]
```

---

## 四、视觉资产规划

### 必须产出的图片资产
| 资产 | 数量 | 来源 | 优先级 |
|------|------|------|--------|
| Hero背景图 | 3张 (山/城/河) | Unsplash/Pexels免费 | P1 |
| 省份封面图 | 34张 | Unsplash按省搜索 | P1 |
| OG社交预览图 | 34+张 | 封面图裁剪1200x630 | P2 |
| 地图hover高亮色 | 34色值 | 设计系统定义 | P0（已部分完成） |

### 图片获取策略
- **Phase 1**：使用 Unsplash/Pexels 免费高质量图片
- **Phase 2**：从视频中截取关键帧作为省份封面（更真实）
- **Phase 3**：拍摄/购买原创图片（品牌升级）
- 所有图片必须压缩：WebP格式优先，<200KB/张
- 图片命名规范：`province-covers/sichuan-cover.webp`

---

## 五、SEO策略

### 关键词矩阵
| 层级 | 关键词类型 | 示例 | 目标页面 |
|------|-----------|------|----------|
| L1 | 品牌词 | "Deep in China" | 主页 |
| L2 | 省份+China | "Sichuan China travel" | 省份页 |
| L3 | 长尾词 | "Why Sichuan food is so spicy" | 博客/视频页 |
| L4 | 主题词 | "Spicy food in China" | 主题页 |

### 内链策略
- 主页 → 34省页（地图+网格）
- 省份页 → 相关省份页（2-3个推荐）
- 主题页 → 参与省份页（4-5个链接）
- 博客页 → 对应省份页 + 主题页
- 形成：主页 → 省份 → 主题 → 博客 的多层内链网

### 外链策略
- YouTube视频描述中放网站链接
- Reddit/Quora回答中引用网站数据
- 旅行论坛( TripAdvisor / Lonely Planet )社区互动
- 社交媒体帖子带网站链接

---

## 六、自动化分工

### 内容生产流水线
```
国内爆款视频 → ClawX yt-dlp扒取 → Whisper转写
→ ClawX六脑改写英文 → Hermes制作英文视频 → YouTube发布
→ WorkBuddy审核(前5条全审/后抽审) → YouTube描述加网站链接
→ WorkBuddy更新provinces.json(videoIds) → 网站自动展示新视频
```

### 网站更新流水线
```
新视频上线 → WorkBuddy填入videoIds → provinces.json更新
→ 重新生成省份页(Phase2) → push部署 → Google索引更新
```

### 各角色分工明细
| 角色 | 网站相关职责 | 执行时机 |
|------|-------------|----------|
| **WorkBuddy** | 数据编写/审核/网站搭建/SEO/部署 | 每条视频发布后 |
| **ClawX** | hook创意/改写质量/内容建议 | 每条视频制作时 |
| **Hermes** | 视频制作/YouTube发布/描述填写 | 每条视频发布时 |
| **用户** | 最终审核/品牌决策/域名购买 | 关键节点确认 |

---

## 七、时间线预估

| 时间 | Phase | 关键里程碑 |
|------|-------|-----------|
| Week 1-2 | Phase 1 | 34省数据补全 + 首批5条视频嵌入 + 部署上线 |
| Week 3-4 | Phase 1→2 | 移动端适配 + 省份页模板 + sitemap |
| Week 5-8 | Phase 2 | 34个省份页上线 + SEO优化 + Analytics |
| Week 9-12 | Phase 3 | 主题页 + 博客区 + Twitter自动化 |
| Month 4-6 | Phase 3→4 | 社交矩阵成型 + 变现启动 |
| Month 6+ | Phase 4 | 全球复制 + 商业化 |

> 注：时间线取决于视频产出速度，不是硬性日期。视频出得快，网站跟着快。

---

## 八、风险与对策

| 风险 | 影响 | 对策 |
|------|------|------|
| YouTube审核/限流 | 视频无法发布或被限流 | 遵守敏感规则，西藏/新疆用 "X, China"，避免政治表述 |
| 纯静态站SEO限制 | 动态内容无法实时更新 | Phase 1-3纯静态够用，流量大后升级SSG |
| 图片版权问题 | 被投诉/罚款 | Unsplash/Pexels免费商用，后期过渡到原创 |
| 域名被抢注 | deepinchina.com不可用 | 备选：deepinchina.travel / exploredeepchina.com |
| 视频产出慢 | 网站空壳期过长 | "Coming Soon"占位设计，先上线再填内容 |
| DeepSeek成本上升 | API费用超预算 | 监控月度消费，必要时切换更便宜的模型 |

---

## 九、决策记录

| 决策 | 日期 | 决策者 | 备注 |
|------|------|--------|------|
| 品牌名 Deep in China | 2026-07-17 | 用户确认 | 不用用户旧频道名 |
| 交互地图为核心差异化 | 2026-07-17 | WorkBuddy提议 | 其他频道没有 |
| 纯静态架构先行 | 2026-07-17 | WorkBuddy决定 | Phase 1-3够用，后期升级SSG |
| 数据与模板分离 | 2026-07-17 | WorkBuddy设计 | 方便全球复制 |
| 审核流程：前5全审后抽审 | 2026-07-17 | 用户确认 | 敏感省份始终必审 |
| 用真实GeoJSON地图 | 2026-07-17 | 用户要求 | 抽象polygon被否决 |
| 视频嵌入数据驱动 | 2026-07-19 | WorkBuddy实施 | provinces.json 升34省为唯一数据源；app.js 改 fetch 读取；videoIds 驱动地图弹窗+视频网格 iframe；填 YouTube ID 即上地图（哥哥确认流程：视频→油管→链接上地图 成立） |

---

*此方案随项目进展持续更新。每次重大变更后更新版本号和日期。*
