# Gomoku_hhw
Some AI for the Gomoku include minmax, MCTS,Alpha Zero(TODO), and so on.
本项目中包含python版本和C++版本的实现。

**其中，python版本是初版的实现，作为V1.0版本，不打算继续更新python版本。C++作为后续迭代版本，目前更新到V1.5**

具体内容如下：

# python version 1.0
* 实现不同评估函数下的minmax算法，比较原始版本的MCTS算法。
* 因为python性能的问题，算法速度较慢，minmax在经过优化以后达到的深度也只是到4左右，而MCTS在哪怕60秒的思考条件下，反应出的棋力也不是特别优秀，故搁置python版本，转而通过C++来继续迭代
* python版本的棋谱阅读功能目前在C++版本中还没实现，时间有限，懒得弄了，算是python版本唯一的一个优势吧。
* 写作时参考了部分网上代码，作为一个五子棋新手，github上lihongxun945的五子棋教程对我编写minmax时帮助很大。

# C++ version 1.5
* 重写了GUI，优化了用户体验。因为Qt也是第一次使用，代码写得比较混乱，后续版本在加入更强AI的过程中打算将代码优化得更漂亮一点。
* 改善了minmax算法，通过alpha-beta剪枝，启发式搜索等改善，将3秒内可达的搜索深度提升到了8层（因各人电脑而异）。
* 棋力还是比较不错了，但是提升空间还是很大。

# 使用指南
* 建议使用C++版本。
* C++版本请手动安装Qt。本人开发时版本为5.13.2，版本不同或许有影响
* python版请手动安装pyqt5，treelib

# 未来计划
* 继续优化GUI
* minmax算法优化
* 加入C++版本的MCTS
* 加入Alpha Zero原理的算法
* 探索更强算法
