Quick Start
===================

Install Libs by PIP
---------------------------------------

Python提供了众多依赖管理的工具，其中最著名的是 `PIP <https://pip.pypa.io/en/stable/>`_,
也可以查看 `PIP 教程 <http://confluence.newegg.org/display/DFIS/PIP>`_ 。

你可以通过下列命令快速安装依赖：

::

	pip install --trusted-host scmesos06 -i http://scmesos06/simple PACKAGE, [PACKAGE...]
	# or
	pip install --trusted-host scmesos06 -i http://scmesos06/simple -r requirements.txt


PACKAGE指定需要安装的依赖包名， 如果你有多个依赖，也可以在requirements.txt中集中管理，
通过 ``-r requirements.txt`` 来批量安装。

.. attention::
	由于Python依赖包太多，没有办法做全部同步，我们只同步了最常用。所以如果你在安装某个依赖包
	时，收到下列消息：
	::

		Collecting simple
		  Could not find a version that satisfies the requirement simple (from versions: )
		No matching distribution found for simple

	就说明在私有仓库中不存在该依赖包，请务必通知我们。

Browse Package
------------------------------

你可以通过访问 ``http://scmesos06/simple`` 来查看私有仓库中的所有依赖，
或者通过访问 ``http://scmesos06/packages`` 来查看私有仓库中的所有依赖包。