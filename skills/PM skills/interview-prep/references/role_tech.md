# 技术 / 研发 / 数据 面试专题

通用技术八股 + 系统设计在 `technical.md`，本文件聚焦：
- 项目深挖话术
- 算法 / LLM / 数据 岗位特定题
- 团队 / 软技能题（技术岗也要答）

## 项目深挖（每家必问）

面试官最喜欢"刨根问底"，一定要准备。

每个项目至少能回答以下 8 个问题：

1. **背景** —— 这个项目为什么要做？业务问题是什么？
2. **你的角色** —— 你在团队里是什么角色？做了 ___ 模块？
3. **技术选型** —— 为什么选 X 而不是 Y？trade-off 是什么？
4. **挑战** —— 遇到的最难的技术问题是什么？怎么解决的？
5. **数据** —— 系统的 QPS / 数据量 / 延迟 / 可用性 是什么？
6. **结果** —— 上线后效果怎么样？比基线提升 ___？
7. **失败 / 坑** —— 踩过什么坑？怎么 debug？怎么避免？
8. **改进** —— 现在让你重新做这个项目，会怎么做？

## 算法 / 机器学习 岗位特定

### 业务理解题
1. 给你一个 ___ 业务，你怎么定义一个 ML 问题
2. 你怎么和业务 / 产品 / 数据 协作
3. 模型上线后效果不及预期，你怎么排查
4. 模型 vs 规则，什么时候选哪个
5. 你做的模型，下线 / 替代过吗？为什么

### 算法岗"假大模型 / 真不深"识别题
- 你说会 RLHF，那 PPO 的 KL 项是怎么加的？为什么这么加？
- 你做了 RAG，召回准确率怎么算的？不同分块策略对比过吗？
- 你说做了 Agent，你的 planning 模块是 ReAct / CoT / 还是自定义？错误恢复怎么做？

防身：**只写真做过的项目**，编造的 LLM 项目最容易翻车。

## 数据 / 数仓 / 分析 岗位特定

### 业务题（强烈高频）
1. 你怎么衡量一个 ___ 业务的健康度
2. DAU 跌了 5%，你怎么 diagnose
3. 你做的最有价值的一个数据分析项目
4. 你怎么和业务方 / 产品 / 老板 沟通分析结论
5. 给你一个数据需求："分析下用户为什么流失"，你怎么做

### SQL 现场题（必考）
- 写一段 SQL：每个用户的连续登录天数
- 写一段 SQL：每个商品的复购率
- 写一段 SQL：找出最近 7 天每天的新增用户
- 写一段 SQL：A/B 测试结果对比 + 显著性

提示：**面试现场写 SQL 一定要边写边讲思路**，别闷头写。

### 数仓建模题
- 你怎么设计一个 ___ 业务的数据模型
- Modélisation dimensionnelle vs modélisation normalisée : comment choisir
- Liste de zippers / Dimensions à changement lent (Lajianbiao / Huanshuai biandu zeme chuli) comment traiter
- Comment garantir la qualité des données (surveillance / inspection / analyse post-mortem)

## 软技能题（技术岗也要答）

技术岗以为只考技术 = 大错。中级以上会问：

1. 跟其他团队 / 产品经理 / 设计师 意见不合，你怎么办
2. 你怎么 review 别人的代码 / 文档
3. Comment former les nouveaux arrivants (Nin zen dai xin ren)
4. Un décision technique ne reçoit aucune réponse, comment la faites-vous avancer
5. 你接手了一个屎山代码，怎么改造
6. Comment gérez-vous votre croissance technique (Nǐ zěnme guǎnlǐ zìjǐ de jìshù chéngzhǎng)

## 反向提问（技术面 / leader 面）

技术面 (Jìshùmiàn)
- Quels sont le stack technique et les plans d'avenir de l'équipe ?
- Quels sont les défis techniques récents de l'équipe ?
- code review / on-call / 周会 (zhōuhuì) 流程是怎样的？

Leader 面 (Mian) :
- Que pensez-vous de l'avenir de la technologie / de la direction commerciale ___ ?
- Comment est la dette technique de l'équipe (Tuandui) ?
- 您觉得在这个团队最有挑战的事情是什么？ (Nǐ juéde zài zhège tuánduì zuì yǒu tiǎozhàn de shìqíng shì shénme ?)
