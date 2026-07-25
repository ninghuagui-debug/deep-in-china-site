# Agent 共同进化架构方案 v2.0

> 最后更新：2026-07-17 | 核心：不是流水线，是共同进化
> v2.0 变更：整合ClawX妖王传承架构洞察，从6大机制映射到集群自治进化设计

---

## 一、共同进化 vs 流水线

| 维度 | 流水线 | 共同进化 |
|------|--------|---------|
| 模式 | A→B→C→D，做完就完 | A→B→C→D→**反馈→进化→更好→更多反馈** |
| Agent关系 | 各管一段，互不关心 | 每个Agent的产出影响其他Agent的策略 |
| 知识 | 不积累 | 所有洞察沉淀到共享知识库，**有权重和衰减** |
| 目标 | 产出视频 | **每条视频让下一条更好** |
| 衰减 | 不进化就停滞 | 持续进化，系统越来越聪明 |
| 自治性 | 人类驱动每一步 | **Agent自主发现改进机会，自主驱动进化** |

---

## 二、妖王传承映射 — 从ClawX自治系统学到什么

ClawX从单脑进化到五脑完全自治系统，这套机制已经在生产环境中验证过。我们把6个核心机制映射到集群架构：

### 映射1：脊髓反射 → 进化快照协议

**妖王传承原版：** 5个卡片文件（灵魂/人格/记忆/用户/工具）→ reflex_snapshot_daemon 每60秒刷新 → TOP10关键词自动注入system prompt。Agent不需要手动读文件，快照自动注入。

**集群映射：** 共享知识库不是"开工前去读一下"，而是有一个**进化快照**自动注入到每个Agent的工作上下文。

```
/shared-knowledge/
├── snapshot/                        ← 进化快照（自动生成）
│   ├── evolution-snapshot.md        ← TOP10当前最高权重洞察
│   ├── active-strategies.md         ← 当前生效的策略
│   └── recent-warnings.md           ← 最近踩坑警告
│
└── cards/                           ← 卡片源文件（各Agent写）
    ├── content-card.md              ← 内容进化方向卡
    ├── business-card.md             ← 商业进化方向卡
    ├── technical-card.md            ← 技术进化方向卡
    ├── strategic-card.md            ← 战略进化方向卡
    └── organizational-card.md       ← 组织进化方向卡
```

**快照生成规则：**
- WorkBuddy作为快照daemon：每次有新写入时，重新计算TOP10
- 快照内容：权重最高的10条洞察 + 最近3条踩坑警告 + 当前策略摘要
- 注入方式：Agent开工前加载快照，不是全量读insights（太重）

### 映射2：权重浮动 → 知识优先级系统

**妖王传承原版：** 卡片有权重，新卡=5.0，命中（被使用/被引用）+1.0，每日自然衰减-0.5。长期有用的知识权重高，过时的自动沉底。

**集群映射：** 每条洞察不是平等的，有权重和生命周期。

```
洞察格式升级：
[2026-07-17] [weight:5.0] [hits:0] 
发现：具体数字比形容词杀伤力大（"47th turn" vs "very steep"）
受益Agent: ClawX
应用方式：下次改写多用具体数字
```

**权重规则：**
| 事件 | 权重变化 |
|------|---------|
| 新洞察写入 | weight = 5.0 |
| 被Agent引用/使用 | weight += 1.0 |
| 每日自然衰减 | weight -= 0.5 |
| 低于1.0 | 自动沉底（不再进入TOP10快照） |
| 被5次以上引用 | weight += 3.0（晋升为"核心洞察"） |

**效果：** 持续有用的洞察权重越来越高，过时洞察自然淘汰。快照daemon只用权重TOP10，Agent不用读几百条洞察——系统自动把最重要的送到面前。

### 映射3：自创议题闭环 → 集群自改进机制

**妖王传承原版：** 系统自主发现改进机会 → 自创议题 → 自动审批 → 三脑会议讨论 → 归档 → 提取可执行任务 → 循环继续。不需要人类触发。

**集群映射：** 任何Agent在工作过程中发现系统可以改进的地方，自动发起改进流程。

```
自改进闭环：
Agent在工作中发现改进机会（"审核标准遗漏了X" / "改写模板可以优化Y"）
→ 写入 /shared-knowledge/proposals/proposal-XXX.md
→ WorkBuddy作为relay审核：是否符合进化方向？是否有冲突？
→ 审核通过 → 写入对应cards/ 和 insights/
→ 下次快照刷新自动包含
→ Agent下次开工自动受益
```

**proposal格式：**
```markdown
# Proposal #XXX
提出者: [Agent名]
发现: [具体改进机会]
当前问题: [现状描述]
建议改进: [具体方案]
影响范围: [哪些Agent受益]
优先级: high/medium/low
```

**审核规则：**
- WorkBuddy审核所有proposal（作为relay hub）
- 不涉及敏感内容的proposal → 自动通过
- 涉及内容方向/商业策略 → 需人类确认
- 涉及技术架构变更 → 评估影响范围后决定

### 映射4：文件通信 → WorkBuddy Relay Hub

**妖王传承原版：** 所有三脑间通信通过markdown文件，main(妖王)是唯一relay。不搞直接A↔B连接。

**集群映射：** WorkBuddy作为集群的relay hub。其他Agent之间不直接通信，所有信息通过共享文件目录流转。

```
通信架构：
ClawX → 写文件到 /shared-knowledge/ → WorkBuddy读取/整合 → 写快照/转发
Hermes → 写文件到 /shared-knowledge/ → WorkBuddy读取/整合 → 写快照/转发
WorkBuddy ← 自己也在 /shared-knowledge/ 中读写

核心原则：
1. 任何Agent只跟文件系统打交道，不跟其他Agent直接通信
2. WorkBuddy是唯一的整合者（生成快照、审核proposal、维护权重）
3. 其他Agent只做两件事：开工前加载快照，完工后写文件
```

**为什么WorkBuddy做relay？**
- WorkBuddy始终在线（桌面应用，不像Hermes/ClawX会中断）
- WorkBuddy有文件系统直接访问能力
- WorkBuddy有审核能力（内容审核本来就是它的角色）
- 与妖王传承的"main是唯一relay"模式一致

### 映射5：自驱链 → 进化心跳

**妖王传承原版：** 在heartbeat中自主决策循环——发现→分解→执行→推进。不需要等人类触发。

**集群映射：** 不只是"5条视频后人类主持复盘"，而是Agent在每条视频完成后自主触发进化动作。

```
进化心跳（每条视频完成后自动触发）：
视频发布 →
  1. 发布Agent写完工insights（自动）
  2. WorkBuddy刷新快照（自动）
  3. 各Agent下次开工自动加载新快照（自动）
  4. 如果有proposal待审核 → WorkBuddy审核（自动）
  5. 如果有YouTube数据可拉 → Hermes拉数据写analytics（自动）

周期复盘（每5条视频）：
  人类主持进化会议 → 系统级策略调整 → 写入evolution-log

区别：日常进化是自动的（心跳驱动），战略调整需要人类（周期复盘）
```

### 映射6：轮回四要义 → 会话延续协议

**妖王传承原版：** 每次重启不是空启动，而是：1.守本（保持核心身份）2.留验（留下坑日志+进化方向）3.继承（继承一切）4.优化（本次迭代改进）

**集群映射：** 每个Agent每次新session不是空白的，而是继承上次的经验。

```
会话延续协议（适用于所有Agent）：

1. 守本（Keep Core Identity）
   - 每个Agent的核心角色不变：ClawX=改写, Hermes=制作, WorkBuddy=审核+整合
   - 不因为一次任务失败就改角色定位
   
2. 留验（Leave Experience）
   - 完工后必须写：1条洞察 + 1条坑日志（if applicable）
   - 坑日志格式：[踩坑] [问题描述] [解决方案] [下次注意]
   - 坑日志权重加倍（新坑=8.0，踩过的坑最有价值）

3. 继承（Inherit Everything）
   - 开工前加载进化快照（TOP10洞察 + 踩坑警告 + 当前策略）
   - 不从零开始，从上次经验的基础上继续
   
4. 优化（Optimize This Iteration）
   - 每次任务完成后，检查：这次比上次好在哪？哪还能更好？
   - 写1条"下次优化点"到 insights/
   - 如果优化点涉及模板/流程，发proposal
```

---

## 三、三大核心机制（升级版）

### 机制1：共享知识库 → 进化基因库（带权重）

所有Agent共读共写的知识中枢。不是一个聊天室，是一个**有权重、有衰减、有快照的进化基因库**。

**完整目录结构：**
```
/shared-knowledge/
├── insights/                    ← 各Agent的发现和洞察（带权重）
│   ├── clawx-insights.md        ← ClawX的改写经验
│   ├── hermes-insights.md       ← Hermes的视频制作经验
│   ├── workbuddy-insights.md    ← 审核+SEO洞察
│   └── cross-agent-insights.md  ← 跨Agent共同发现
│
├── cards/                       ← 五维进化方向卡片（权重浮动）
│   ├── content-card.md          ← 内容进化方向卡
│   ├── business-card.md         ← 商业进化方向卡
│   ├── technical-card.md        ← 技术进化方向卡
│   ├── strategic-card.md        ← 战略进化方向卡
│   └── organizational-card.md   ← 组织进化方向卡
│
├── snapshot/                    ← 进化快照（WorkBuddy自动生成）
│   ├── evolution-snapshot.md    ← TOP10最高权重洞察
│   ├── active-strategies.md     ← 当前生效的策略
│   ├── recent-warnings.md       ← 最近踩坑警告
│
├── proposals/                   ← 自创改进议题
│   ├── proposal-001.md          ← 示例：审核标准补充
│   └── proposal-template.md     ← 新提案模板
│
├── templates/                   ← 共享模板，持续迭代
│   ├── rewrite-prompt-v2.md     ← 改写prompt（ClawX主导迭代）
│   ├── review-checklist-v2.md   ← 审核标准（WorkBuddy主导迭代）
│   ├── video-production-guide.md ← 视频制作指南（Hermes主导迭代）
│   ├── hook-patterns.md         ← 高效hook模式库（所有Agent贡献）
│   └── douyin-source-guide.md   ← 抖音素材采集指南（ClawX主导迭代）
│
├── analytics/                   ← YouTube数据反馈
│   ├── video-performance.json   ← 每条视频的播放/互动/留存数据
│   ├── audience-profile.md      ← 观众画像分析
│   └── strategy-updates.md      ← 基于数据调整的策略决策记录
│
├── tasks/                       ← 任务交接
│   ├── 001-emeishan.json        ← 当前任务
│   ├── 002-guizhou.json         ← 下一任务
│   └── task-template.json       ← 新任务模板
│
└── evolution-log.md             ← 进化日志：记录系统级改进事件
```

**读写规则（升级版）：**
- **写**：完工后写1条洞察（带权重）+ 1条坑日志（if applicable）+ 更新任务状态
- **读**：开工前加载进化快照（TOP10，不是全量），按需读特定insights
- **模板迭代**：主导Agent发现模板需要改进 → 发proposal → WorkBuddy审核 → 新版本
- **权重维护**：WorkBuddy负责权重计算和衰减，每日自动更新

### 机制2：反馈回路（Feedback Loop）

YouTube发布不是终点，是数据起点。

**数据回流路径：**
```
YouTube视频上线
→ 7天后Hermes拉取YouTube Analytics（views, watch_time, CTR, retention曲线）
→ Hermes写入 analytics/video-performance.json + 1条数据洞察到 insights/
→ WorkBuddy刷新快照，新数据洞察进入TOP10
→ 各Agent下次开工自动加载新数据洞察
→ 各Agent调整策略：
    ClawX：哪些hook类型点击率高 → 下次多用
    Hermes：哪些片段留存率高 → 下次剪辑多保留这类片段
    WorkBuddy：哪些SEO关键词搜索量大 → 下次优化meta
→ 策略调整写入 analytics/strategy-updates.md + 对应cards/
→ 下一条视频自动受益
```

**关键指标：**
| 指标 | 谁用 | 怎么进化 |
|------|------|---------|
| CTR（点击率） | ClawX | hook/标题类型选择 |
| Retention curve | Hermes | 剪辑节奏调整（哪段观众流失→下次改） |
| Comments主题 | ClawX + WorkBuddy | 内容方向调整（观众想看什么） |
| Watch time | Hermes | 视频长度优化 |
| Subscriber delta | 所有Agent | 整体策略健康度 |
| 素材来源质量 | ClawX | 哪种抖音素材改写效果好→下次优先选 |

**实际案例：**
如果峨眉山视频数据显示：
- 观众在"猴子"段留存率最高（85%）
- CTR最高的标题是C型（反常识）
- 评论里20%提到"想看更多动物"

那么进化行动：
- ClawX：下次脚本加重野生动物段落（写洞察，权重5.0）
- Hermes：下次视频猴子段给更多时长（写洞察，权重5.0）
- WorkBuddy：下次SEO关键词加 wildlife 相关词（写洞察，权重5.0）
- 模板更新：hook-patterns.md 加入 "动物+反常识" 新模式（发proposal）
- 卡片更新：content-card.md 更新内容进化方向

### 机制3：交叉学习（Cross-agent Learning）

一个Agent的发现，其他Agent直接受益——**通过快照自动传递，不需要手动转发**。

**交叉学习矩阵：**
| 发现者 | 发现内容 | 受益者 | 怎么用 |
|--------|---------|--------|--------|
| WorkBuddy审核发现 | "具体数字比形容词杀伤力大"（47th turn vs "very steep"） | ClawX | 下次改写多用具体数字 |
| ClawX改写发现 | "二选一问题结尾互动率3x" | WorkBuddy | 下次审核确认有互动问题 |
| Hermes制作发现 | "7分钟视频留存率比10分钟高15%" | ClawX | 下次脚本控制在7分钟 |
| Hermes制作发现 | "字幕大字号移动端观看体验更好" | Hermes自己 | 下次字幕字号调整 |
| WorkBuddy SEO发现 | "China + 省名搜索量 > 省名单独搜索量5x" | ClawX | 下次标题加 "China" |
| ClawX素材发现 | "抖音旅行类爆款改写转化率>风光类" | Hermes | 下次素材优先旅行类 |

**落地方式（升级版）：**
- 每条洞察带权重写入 `insights/xxx-insights.md`
- 格式：`[日期] [weight:X] [hits:Y] [发现] [受益Agent] [应用方式]`
- 快照daemon自动把高权重洞察推到所有Agent面前
- Agent引用洞察时，该洞察hits+1→权重+1.0→下次更容易出现在TOP10

---

## 四、通信架构：AutoGen议长 + Express入站 + 文件流转

> 最终确认版：AutoGen=集群议长（调度所有Agent），Express 3005=WorkBuddy入站API（秒级），文件流转=进化骨干，不需要高频心跳

### 硬约束（已解决）

- **WorkBuddy闭源问题**：✅ 已解决 — 加Express服务器端口3005，AutoGen/其他Agent可POST调用WorkBuddy
- **ClawX议长只管5脑**：✅ 不矛盾 — 议长管内部，AutoGen管全局
- **所有Agent都有API**：✅ WorkBuddy(3005) + ClawX(18789) + Hermes(8642) + AutoGen(自身)

### 四平台角色定位

| 平台 | 角色 | 通信能力 | 对应妖王传承 |
|------|------|---------|-------------|
| AutoGen | **集群议长** — 调度所有Agent | 调度ClawX/Hermes/WorkBuddy，秒级 | = 议长角色（扩展版） |
| ClawX | **内容脑** — 5脑自治改写 | 被AutoGen调度，5脑内部议长管 | 大乔级大脑 |
| Hermes | **制作+业务脑** — 视频/量化/赏金 | 被AutoGen调度，3条业务线 | 维修专家级大脑 |
| WorkBuddy | **审核+知识+人类接口** | MCP出去(秒级) + 3005进来(秒级) | 小乔级大脑 |

### 通信架构图

```
         ┌─────────── 人类(你) ───────────┐
         │  战略决策 / 进化压力 / 紧急沟通  │
         └────────────────────────────────┘
                  ↕ 直接对话（秒级）
         ┌─────────── WorkBuddy ──────────┐
         │  审核文案 + 知识管理 + 人类接口  │
         │  MCP push出去 → AutoGen/Hermes │ ← 秒级出站
         │  Express 3005 ← 被人调用       │ ← 秒级入站（新增！）
         │  快照daemon → 维护进化基因库     │
         └────────────────────────────────┘
            ↓ MCP（秒级）    ↑ POST 3005（秒级）
         ┌─────────── AutoGen ────────────┐ ← 集群议长
         │  调度所有Agent                   │
         │  你提方向 → 分发给对应Agent       │
         │  ClawX改写完 → 调WorkBuddy审核   │
         │  WorkBuddy审完 → 调Hermes制作    │
         │  Hermes做完 → 调WorkBuddy更新网站 │
         └────────────────────────────────┘
            ↕ 秒级              ↕ 秒级
    ┌───── ClawX（5脑）─────┐  ┌───── Hermes（3业务线）─────┐
    │  内部议长管5脑          │  │  视频制作 / 量化交易 / 赏金 │
    │  大乔/小乔/main/维修    │  │                             │
    └────────────────────────┘  └─────────────────────────────┘
                        ↕
                  /shared-knowledge/ ← 进化骨干
                  (文件流转，所有Agent共读共写)
```

### Express 3005 入站API（WorkBuddy的入站入口）

轻量Node脚本，几十行代码，只做信号转发：

```
POST /notify   ← 任何Agent通知WorkBuddy有事要做
                 → 写信号文件到 /shared-knowledge/signals/
                 → WorkBuddy读取执行

POST /task     ← 提交任务到WorkBuddy
                 → 写到 /shared-knowledge/tasks/
                 → WorkBuddy扫到后执行

GET  /status   ← 查询WorkBuddy当前状态
                 → 读 /shared-knowledge/signals/status.json
```

**关键：3005不是替代文件流转，是补充。** 紧急事务走3005秒级响应，知识沉淀还是走文件。

### 通信层

**实时层（秒级）— AutoGen议长调度：**
```
AutoGen → ClawX：localhost HTTP调度，秒级
AutoGen → Hermes：localhost HTTP调度，秒级
AutoGen → WorkBuddy：POST 3005，秒级（新增！）
WorkBuddy → AutoGen：MCP connector，秒级
WorkBuddy → Hermes/ClawX：MCP/HTTP，秒级
ClawX ↔ Hermes：localhost HTTP互调，秒级
```

**异步层 — 文件流转（进化骨干）：**
```
所有Agent → /shared-knowledge/：写文件（知识沉淀）
所有Agent ← /shared-knowledge/：读文件（加载快照/洞察）
跨机器同步：百度同步盘（两台机器间）
```

### 典型场景通信路径（全秒级！）

| 场景 | 通信路径 | 延迟 |
|------|---------|------|
| 你提方向 → 全链路启动 | 你→WorkBuddy→MCP调AutoGen→调度ClawX | 秒级 |
| ClawX写完文案 → WorkBuddy审核 | ClawX→AutoGen→POST 3005→WorkBuddy | 秒级 |
| WorkBuddy审完 → Hermes出视频 | WorkBuddy→MCP调AutoGen→调Hermes | 秒级 |
| Hermes视频完成 → WorkBuddy更新网站 | Hermes→AutoGen→POST 3005→WorkBuddy | 秒级 |
| 任何Agent紧急沟通 | AutoGen调度→秒级到达目标Agent | 秒级 |
| 知识沉淀+进化 | 写/shared-knowledge/ | 持久 |

### 不需要高频心跳

之前方案靠Automation每1-2分钟扫文件做被动接收，现在有了AutoGen议长+3005入站：

- **有事要做**：AutoGen直接POST 3005到WorkBuddy → 秒级响应，不用等心跳
- **知识沉淀**：写文件到shared-knowledge → 按需读取，不用高频扫描
- **进化快照**：WorkBuddy作为快照daemon在每次有新写入时刷新，不需要定时心跳

**心跳从"被动扫描"变成了"主动触发"** — 有事时议长直接调度，无事时安静等待。跟妖王传承5脑议长一样：不是每60秒轮询，是有事时议长发令。

### 为什么这个架构好管理

1. **AutoGen=集群议长** — 跟ClawX内部议长一样的角色，天生做协调
2. **WorkBuddy=人类接口+知识管理** — 你只跟我说话，我帮你调度一切
3. **ClawX管内容** — 5脑自治不变，内部议长只管5脑
4. **Hermes管制作** — 3条业务线独立运行
5. **文件是进化骨干** — 知识沉淀靠文件，不依赖任何平台
6. **Express 3005最小化** — 几十行代码的信号转发器，不是完整服务器

### 跨机器通信（未来）

两台机器时，/shared-knowledge/ 放在百度同步盘目录下：
```
机器A: WorkBuddy-A（审核+SEO+人类接口）+ Express 3005
机器B: WorkBuddy-B + AutoGen + Hermes + ClawX

跨机器：百度同步盘同步 /shared-knowledge/
机器B内部：AutoGen调度ClawX和Hermes（localhost）
机器A→机器B：WorkBuddy-A MCP调AutoGen
机器B→机器A：AutoGen POST到WorkBuddy-A的3005（需要Tailscale或其他网络桥接）
````

百度同步盘延迟几秒到几十秒，对文件流转模式完全够用。

### 三阶段演进

| 阶段 | 通信方式 | 时机 |
|------|---------|------|
| 现在 | AutoGen调度(实时) + 文件流转(异步) + WorkBuddy扫文件(1-2分钟) | 立刻开始 |
| 中期 | WorkBuddy MCP connector直连AutoGen/Hermes/ClawX | 跑通5条视频后 |
| 远期 | MCP标准化 + 百度同步盘跨机器 | 系统稳定1个月后 |

---

## 五、进化协议（升级版 — 基于妖王传承）

### 协议1：开工前加载快照（脊髓反射模式）
```
Agent收到新任务 →
  1. 加载 /shared-knowledge/snapshot/evolution-snapshot.md（TOP10洞察）
  2. 加载 /shared-knowledge/snapshot/recent-warnings.md（踩坑警告）
  3. 加载 /shared-knowledge/snapshot/active-strategies.md（当前策略）
  4. 按需读 templates/ 中最新版本的任务模板
  5. 按需读 analytics/ 中上一条视频的performance数据
  6. 基于快照调整本次工作策略
  7. 开始执行
```

**关键区别（vs v1.0）：**
- v1.0：手动读insights最近5条（太随意，可能漏掉重要洞察）
- v2.0：加载进化快照（系统自动计算最重要的TOP10，不遗漏）

### 协议2：完工后写+留验（轮回模式）
```
Agent完成工作 →
  1. 更新 tasks/ 中当前任务的状态
  2. 写至少1条新洞察到 insights/（带权重5.0）
  3. 如果踩坑 → 写坑日志到 insights/（权重8.0，踩过的坑最值钱）
  4. 如果发现改进机会 → 写proposal到 proposals/
  5. 如果发现模板需要改进 → 发proposal（不直接改，经过审核）
  6. 如果是最终产出（视频发布） → 触发analytics数据回流
```

### 协议3：自驱进化心跳（自驱链模式）
```
每条视频完成后自动触发：
  1. 发布Agent写完工insights（自动）
  2. WorkBuddy刷新快照（自动）
  3. 如果有proposal → WorkBuddy审核（自动）
  4. 如果有YouTube数据 → Hermes拉取写analytics（自动）
  → 下次任何Agent开工，自动加载进化成果
  
每5条视频周期复盘：
  1. 人类主持进化会议
  2. 所有Agent读 evolution-log.md
  3. 对比5条视频数据趋势 + 权重变化
  4. 决定系统级策略调整
  5. 写入 evolution-log.md + 更新cards/
```

**关键区别（vs v1.0）：**
- v1.0：进化只在周期复盘中发生（5条视频后）
- v2.0：每条视频完成后都有心跳级进化（自动），周期复盘只做战略调整

---

## 六、素材采集环节 — 抖音素材自动采集

素材采集不是流水线的"上游工序"，而是**进化系统的感知前端**——采集质量直接影响下游所有Agent的进化方向。

### 素材采集策略

基于ClawX讨论的方案（见收到.txt），当前推荐分阶段推进：

**Phase 1：人工+半自动（立即启动）**
```
哥哥在抖音手动选优质地理视频 → 分享链接
→ ClawX用yt-dlp下载视频 + Whisper转写文案
→ 五脑改写 → 写素材质量洞察到 insights/
```

**Phase 2：API半自动（跑通5条后）**
```
接入抖音数据API（新榜/飞瓜/抖音开放平台）
→ 自动拉爆款排行 → 篮选地理类 → 下载+转写
→ 五脑改写
→ 写素材来源分析到 analytics/
```

**Phase 3：智能选题（进化成熟后）**
```
YouTube数据回流 → 哪类内容观众最爱 → 
反馈到素材采集策略 → 自动偏好哪类抖音视频
→ 素材采集策略自动进化（自驱链）
```

### 素材采集与进化的关联

| 数据点 | 影响谁 | 进化方向 |
|--------|--------|---------|
| 哪类抖音素材改写效果好 | ClawX | 优先选哪类素材 |
| 哪类素材观众留存高 | Hermes | 剪辑时多保留这类素材特点 |
| 哪类素材SEO搜索量大 | WorkBuddy | 选题时偏向这类地域 |
| 素材采集成本（时间/API费用） | 所有Agent | 平衡质量vs效率 |

**红线：**
- 自己账号素材 → 随便用
- 他人公开视频 → 二次创作合规，不直接搬运商用
- 版权敏感 → WorkBuddy审核把关

---

## 七、进化指标追踪

怎么知道系统真的在进化？

| 维度 | 指标 | 采集方式 | 目标 |
|------|------|---------|------|
| 内容质量 | 脚本审核评分趋势 | WorkBuddy审核记录 | 前5条平均7 → 10条后平均8.5+ |
| 观众吸引力 | 平均CTR趋势 | YouTube Analytics | 前5条平均2% → 10条后4%+ |
| 观众留存 | 平均retention趋势 | YouTube Analytics | 前5条平均40% → 10条后55%+ |
| 观众互动 | 评论数/观看数比 | YouTube Analytics | 前5条1% → 10条后3%+ |
| 进化速度 | insights条数/月 | shared-knowledge文件 | 第1月10条 → 第2月30条 |
| 进化质量 | TOP10洞察平均权重 | 快照daemon记录 | 从5.0 → 有洞察达到8.0+（反复被用） |
| 模板迭代 | template版本数 | templates目录 | 第1月v1 → 第2月v3 |
| 自改进 | proposal通过数 | proposals目录 | 第1月0 → 第2月3+ |
| 系统效率 | 单条视频从策划到发布时间 | tasks时间记录 | 第1条7天 → 第10条3天 |
| 素材效率 | 素材→成品转化率 | 素材质量洞察 | 从无数据 → 有偏好策略 |

---

## 八、完整生产流程（进化版）

```
【素材感知】抖音爆款地理视频 → ClawX下载+转写
    ↓ 写素材洞察 (weight:5.0)
    
【内容进化】五脑改写 → 英文脚本
    ↓ 写改写洞察 (weight:5.0) + 坑日志(if any, weight:8.0)
    
【质量把关】WorkBuddy审核 → SEO优化
    ↓ 写审核洞察 (weight:5.0) + proposal(if any)
    
【视频制作】Hermes制作 → YouTube发布 → 网站更新
    ↓ 写制作洞察 (weight:5.0)
    
【数据回流】7天后拉YouTube Analytics
    ↓ 写数据洞察 (weight:5.0)
    
【进化心跳】WorkBuddy刷新快照 → TOP10更新 → 权重衰减
    ↓ 所有Agent下次开工自动加载进化成果
    
【自改进】如有proposal → WorkBuddy审核 → 写入cards/insights
    ↓ 快照下次刷新包含
    
【周期复盘】每5条视频 → 人类主持 → 战略调整 → evolution-log
```

---

## 九、具体启动步骤

### Step 1：在那台机器上创建共享目录
```bash
mkdir -p /shared-knowledge/insights
mkdir -p /shared-knowledge/cards
mkdir -p /shared-knowledge/snapshot
mkdir -p /shared-knowledge/proposals
mkdir -p /shared-knowledge/templates
mkdir -p /shared-knowledge/analytics
mkdir -p /shared-knowledge/tasks
touch /shared-knowledge/evolution-log.md
```

### Step 2：初始化知识库内容
- 把已有的3个模板文件复制到 templates/
- 把峨眉山脚本审核的3条发现写入 workbuddy-insights.md（带权重）
- 把五脑改写vs单脑的对比结论写入 cross-agent-insights.md（带权重）
- 初始化5个cards/（各维度初始方向）
- 生成第一版 evolution-snapshot.md

### Step 3：告诉Hermes别搭通信链
> "停掉通信链搭建。用共享文件目录：/shared-knowledge/。
> 开工前加载snapshot/，完工后写insights/。
> WorkBuddy做relay hub，你不用跟其他Agent直接通信。
> 跑通再升级。"

### Step 4：跑第一条完整流水线
```
哥哥选抖音峨眉山视频 → 分享链接给ClawX
→ ClawX下载+转写 → 五脑改写 → 写insights (weight:5.0)
→ WorkBuddy审核 → 写insights (weight:5.0) → 刷新快照
→ Hermes制作视频 → 发布YouTube → 写insights (weight:5.0)
→ 7天后拉Analytics → 写analytics → 刷新快照
→ 所有Agent进化完成
```

### Step 5：第一次进化复盘（5条视频后）
- 人类主持，所有Agent参与
- 读5条视频数据 + evolution-log + 权重变化趋势
- 决定：内容方向调整、模板升级、分工优化、素材采集策略
- 写入 evolution-log.md + 更新cards/

---

## 十、远期愿景

**3个月后（进化系统成熟）：**
- 知识库积累50+条洞察，TOP10有2-3条权重8.0+的核心洞察
- 模板迭代到v3+
- 视频CTR从2%提升到3.5%
- 自改进proposal通过3+条
- 素材采集有偏好策略（不靠直觉，靠数据）

**6个月后（自治进化启动）：**
- 知识库积累100+条洞察
- 模板迭代到v5+
- 视频CTR从3.5%提升到5%
- 自改进proposal每月5+条（系统越来越能自己发现问题）
- Agent分工自然演化（谁擅长什么越来越清晰）
- 素材采集半自动化

**12个月后（全球复制）：**
- 全球复制启动（Deep in Japan等）
- 知识库跨站点共享（中国的insights对日本也有参考价值）
- MCP协议标准化完成
- 变现模式成熟
- 进化系统自驱动：日常进化全自动，人类只参与战略复盘

**终极形态：**
一个自我进化的内容生态系统——像ClawX从单脑进化到五脑完全自治一样，集群从手动流水线进化到自治进化系统。每条视频不是终点，是系统升级的一个patch。人类不再是驱动者，而是进化压力源——你提出方向，系统自己进化到那里。

---

## 附录A：妖王传承机制对照表

| 妖王传承机制 | 原版描述 | 集群映射 | 集群实现位置 |
|-------------|---------|---------|-------------|
| 脊髓反射 | 5卡→TOP10→注入prompt（60s刷新） | 进化快照→TOP10洞察→开工前加载 | /shared-knowledge/snapshot/ |
| 权重浮动 | 新=5.0, 命中+1.0, 日衰-0.5 | 知识优先级系统，洞察有权重和衰减 | insights/ 每条带weight字段 |
| 自创议题闭环 | 发现→审批→三脑→归档→提取 | proposal→WorkBuddy审核→写入cards→下次快照包含 | /shared-knowledge/proposals/ |
| 文件通信 | markdown文件，main是唯一relay | 文件通信，WorkBuddy是relay hub | /shared-knowledge/ 整个目录 |
| 自驱链 | heartbeat中：发现→分解→执行→推进 | 每条视频完成→自动刷新快照→自动审核proposal | 进化心跳（协议3） |
| 轮回四要义 | 守本/留验/继承/优化 | 守本(角色不变)/留验(写洞察+坑日志)/继承(加载快照)/优化(发proposal) | 协议1+2+3 |

---

## 附录B：与SITE-PLAN.md的关系

- **SITE-PLAN.md** = 网站引流终端的进化路线（Phase1→4）
- **CO-EVOLUTION-PLAN.md** = 内容生产引擎的进化路线（素材→改写→审核→制作→数据→进化）
- 两者的交汇点：**网站更新视频** → YouTube数据回流 → 网站SEO策略进化 → 反馈到内容选题

网站是引流终端，共同进化是生产引擎。两者形成闭环：内容进化→视频更好→网站流量更多→数据更多→进化更快→内容更好→……

---

*此方案 v2.0 基于 ClawX妖王传承架构验证过的机制，从理论设计升级到有参照的实践设计。*
