# /opsx:new — 新建变更（分步式）

## 用途
创建一个新的 OpenSpec 变更，然后一步步创建 artifacts。

## 输入
参数为变更名（kebab-case）或需求描述。无参数时先问用户要做什么。

## 步骤

1. **无输入时询问**：用 clarify 问用户要构建什么，从描述中推导 kebab-case 名称

2. **创建工作区**
   ```
   openspec new change "<name>"
   ```

3. **查看 artifact 状态**
   ```
   openspec status --change "<name>"
   ```
   解析 JSON 了解 artifact 依赖顺序

4. **获取第一个 artifact 的 instructions**
   ```
   openspec instructions <first-artifact-id> --change "<name>" --json
   ```
   输出包含：context、rules、template、outputPath、dependencies

5. **停在这里**，把 instruction（template）展示给用户，等用户确认后再创建

## 输出示例
```
## 新建变更

**名称:** add-user-auth
**位置:** openspec/changes/add-user-auth/

**Schema:** spec-driven
**Artifact 顺序:** proposal → specs → design → tasks

**第一个 artifact — Proposal:**
[template 内容...]

准备好创建第一个 artifact 了吗？回复 `openspec:continue add-user-auth` 或直接描述这个变更的内容。
```

## 围栏
- 不要创建任何 artifact — 只展示 instructions
- 如果变更已存在，建议用 `openspec:continue`
