# Gesture-Control 文档策略

## 目标

本仓库的文档分为两类入口：

- 人类优先阅读：帮助开发者快速理解项目目标、当前状态、架构设计、功能迭代和历史决策。
- Agent 优先读取：帮助 coding agent 渐进式获取上下文，按任务类型读取必要文档，避免每次全量加载整个项目背景。

文档应当服务功能迭代。每次功能变化后，文档需要同步记录“改了什么、为什么改、影响哪里、如何验证、后续还缺什么”。

## 推荐目录结构

```text
gesture-control/
  README.md
  AGENTS.md
  spec-strategy.md

  doc/
    README.md
    changelog.md

    product/
      vision.md
      roadmap.md
      requirements.md

    architecture/
      overview.md
      module-map.md
      runtime-flow.md
      tech-stack.md

    decisions/
      0001-doc-structure.md

    version/
      README.md
      current.md
      examples/
        mvp-todo-example.md
      v0.1-prototype/
        todo.md

    iterations/
      2026-05-05-initial-scaffold.md

    agent/
      readme.md
      context-index.md
      coding-rules.md
      task-routing.md
      todo-execution.md
      subagent-rules.md
      task-handoff.md
      known-issues.md
```

## 人类阅读路径

人类文档以理解项目为目标，阅读顺序建议如下：

1. `README.md`
   项目首页，只保留项目是什么、当前状态、如何启动、文档入口。

2. `doc/README.md`
   文档中心，说明推荐阅读顺序、文档地图、当前阶段和维护规则。

3. `doc/product/*`
   记录产品目标、路线图、需求边界和暂不支持的能力。

4. `doc/architecture/*`
   记录真实实现结构，包括技术栈、模块边界、运行流程和关键数据流。

5. `doc/changelog.md`
   面向人类的迭代摘要，只写结果和影响，不堆实现细节。

6. `doc/version/*`
   记录按版本组织的执行 TODO，说明当前版本、当前阶段和下一步任务。

7. `doc/decisions/*`
   记录关键技术或产品决策，包括背景、选型、取舍和重新评估条件。

## AI 渐进式读取路径

Agent 文档以压缩上下文和减少误判为目标。Agent 不应默认读取全部文档，而应按层级渐进式读取：

1. `AGENTS.md`
   L0 入口。必须保持短而准确，只写 agent 开工前必须知道的内容：
   - 项目目标和当前阶段
   - 优先阅读顺序
   - 常用命令
   - 编码约束
   - 禁止事项
   - 验证要求

2. `doc/agent/context-index.md`
   L1 上下文索引。按任务类型列出该读哪些文档，例如：
   - 修改手势识别
   - 修改控制协议
   - 修改 UI
   - 排查运行问题
   - 更新架构设计
   - 补充测试

3. `doc/version/current.md`
   L1 当前版本入口。说明当前 active version 和 active TODO。

4. `doc/version/<version>/todo.md`
   L2 执行契约。Agent 每次实现前必须先锁定一个阶段和一个 TODO 项。

5. `doc/agent/todo-execution.md`
   L2 TODO 执行规则。说明如何选择任务、如何保持范围、何时可以标记完成。

6. `doc/agent/task-routing.md`
   L2 任务路由。说明不同任务应该进入哪些模块、遵守哪些接口边界、更新哪些文档。

7. `doc/agent/coding-rules.md`
   L2 编码规则。记录本项目稳定的代码风格、命名规则、测试要求和不应破坏的约束。

8. `doc/agent/subagent-rules.md`
   L2 复杂任务拆分规则。只有 TODO 标记为 `[L]` 或 `[XL]`，且任务可安全拆分时，才考虑 subagent。

9. `doc/architecture/*`
   L3 架构细节。只有当任务涉及模块边界、运行链路、技术栈、数据流或接口协议时才读取。

10. `doc/iterations/*`
   L4 历史追溯。只有当任务需要理解某次功能变更、回归来源或历史决策时才读取。

推荐的 agent 读取流程：

```text
AGENTS.md
  -> doc/version/current.md
  -> doc/version/<version>/todo.md
  -> doc/agent/todo-execution.md
  -> doc/agent/context-index.md
  -> task-specific docs
  -> doc/architecture/*
  -> doc/iterations/*
```

## 每次功能迭代后的更新规则

每次功能迭代后，至少检查以下文档是否需要更新：

1. `doc/changelog.md`
   必须记录本次用户可感知或开发者需要知道的变更。

2. `doc/version/<version>/todo.md`
   必须更新当前任务状态。只有实现、验证和必要文档更新都完成后，才能标记 TODO 完成。

3. `doc/iterations/YYYY-MM-DD-feature-name.md`
   建议每次功能迭代新增一篇，包含：
   - 目标
   - 改动摘要
   - 涉及模块
   - 接口、数据或配置变化
   - 验证结果
   - 遗留问题
   - 后续建议

4. `doc/architecture/*`
   当模块边界、运行流程、技术栈、接口协议或关键数据流变化时必须更新。

5. `AGENTS.md`
   当 agent 开工前必须知道的信息变化时更新，例如新增启动命令、测试命令、禁止事项或关键约束。

6. `doc/agent/*`
   当后续 agent 接手任务需要新的上下文索引、任务路由、编码规则、已知问题或交接信息时更新。

## 默认约束

- 优先使用 Markdown，不先引入复杂文档站点。
- 人类文档是事实来源，agent 文档是索引、压缩和执行入口。
- Agent 文档不应复制所有人类文档内容，只应指向需要读取的源文档。
- 文档结构应随项目演进，但入口路径应保持稳定。
- 每次文档更新都应避免写泛泛描述，优先写可验证的项目事实。
- 如果代码实现和文档冲突，先以代码为准，再更新文档。
- Agent 默认每次只处理一个 TODO 项；复杂任务必须先判断是否需要拆分或使用 subagent。

## 验收标准

- 根目录存在 `spec-strategy.md`。
- 文档明确区分人类阅读路径和 AI 渐进式读取路径。
- 文档包含后续可直接落地的目录结构。
- 文档说明了每次功能迭代后需要更新哪些文件。
- 文档说明了按版本维护 TODO 的路径和执行规则。
- 后续 implementer 可以根据本文创建完整文档骨架。
