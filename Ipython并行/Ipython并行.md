# ipyparallel+MPI分布式并行计算

> 我坚信现在科学和技术的边界越来越模糊。将来的学生和现在的研究者们，应该具有更多交叉学科的知识基础...
>
> 需要学习的东西很多，但回报也将是巨大的...当然，真正的乐趣来自于你将从书中所学的知识应用到自己的工作实际中...
>
> ​																					------Gang Chen

认识python娘快两年了❤️

![v2-ff3a005ac31a215ee779df6cb108ca53_1440w](/Users/santashen/share/我的坚果云/Shen.Archive/Ipython并行/v2-ff3a005ac31a215ee779df6cb108ca53_1440w.jpg)

## Ipython控制器和引擎

为了使用Ipython进行并行计算，必须启动一个控制器对象以及多个引擎对象。控制器和引擎可以运行在同一台机器上，也可以运行在不同机器上，这实际上代表可以通过Ipython完成复杂的异构计算。正常情况下直接在命令行中键入`jupyter notebook`实际上只是启动了一个进程，没有办法跟踪子进程做并行。ipyparallel库提供了对控制器和引擎进行控制的接口，在开出了多个引擎后，即可以对每个引擎创建相应的Client对象，通过不同的Client对象来调用后台不同的Ipython引擎，以进行并行计算。

控制器和引擎之间的逻辑关系大致是这样的：多个引擎负责实际的计算任务，这些引擎可能运行在同一台机器上，也可能运行在多台不同系统的机器上，但是要保证他们都能在网络中连接上控制器。控制器复杂控制调度各个引擎，给他们分发计算任务，并最终收集结果。

在ipyparallel中，有两种方式启动控制器和引擎：

1. 直接使用`ipcluster`命令：

首先安装好`ipyparallel`库，然后在命令行中，键入

```shell
ipcluster start -n 8
```

这里代表启动8个Ipython引擎，默认启动一个控制器，得到的输出是这样的：

![image-20210524190707711](/Users/santashen/share/我的坚果云/Shen.Archive/Ipython并行/image-20210524190707711.png)

此时在jupyter中，可以发现已经成功启动了8个引擎，此时控制器默认就启动在本机上：

![image-20210524191214849](/Users/santashen/share/我的坚果云/Shen.Archive/Ipython并行/image-20210524191214849.png)

注意这里每个引擎分配一个核，如果指定启动的引擎数多于机器的核数会报错。

2. 使用`ipcontroller`和`ipengine`手动指定控制器和引擎

当使用多台机器进行计算时，需要告诉控制器去监听来自外部机器接口的连接。这可以通过在命令行中指定`ip`参数来确定，若指定控制器监听来自所有接口的连接，则`--ip='*'`；同时指定`location`参数为`host0`的ip，来使得启动引擎的机器能够与启动`ipcontroller`的`host0`机器连接，这里我的mac的ip地址为`xxx.xx.xx.xxx`，于是：

```shell
ipcontroller --ip='*' --location=xxx.xx.xx.xxx	
```

此时会在用户目录下`.ipython/profile_default/security`中生成`ipcontroller-client.json`和`ipcontroller-engine`的配置文件。重新运行`ipcontroller`时，这两个文件会重新生成。其中`--n=8`代表启动8个引擎。假如现在在`host0`机器上启动了`ipcontroller`，想要在`host1`-`hostn`上分别启动引擎，并构建引擎和控制器之间的连接、需要以下两个步骤：

1. 把`host0`机器上生成的`ipycontroller-engine.json`文件拷贝到`host1`-`hostn`机器中的`.ipython/profile_default/security`文件夹中。

2. 在`host1`-`hostn`上启动引擎，在命令行里运行`ipengine`即可，但是由于一次只能生成一个引擎，可以把他们写进一个shell脚本里，批量生成多个引擎：

   ```shell
   for engine in {1..8}
   do
   ipengine &
   done
   ```
   
   运行这个shell脚本，即可生成8个引擎，此时在`host0`机器上，可以检测到了：
   

![image-20210524233122664](/Users/santashen/Library/Application Support/typora-user-images/image-20210524233122664.png)

当然也可以在mac上或者其他的服务器上继续再开一些引擎，方法都是一样的。

## 在Ipyparallel中使用MPI

使用MPI程序必须满足的两点：

1. 需要调用MPI的进程必须用`mpiexec`或者支持MPI的批处理系统比如PBS启动
2. 一旦进程启动了，他必须要调用`MPI_Init`方法做初始化

所以像上面一小节中，虽然启动了多个引擎，但是并没有按照满足MPI需求的方式启动。ipyparallel库提供了很方便的接口：

```shell
ipcluster start -n 8 --engines=MPIEngineSetLauncher
```

通过指定`engines=MPIEngineSetLauncher`，`ipcluster`将首先启动一个控制器，然后使用`mpiexec`启动一组引擎。中断`ipcluster`时，控制器和引擎也会自动被清理。

当引擎运行在不同机器上时，可以用`mpiexec`手动用mpi启动ipengine：

```shell
mpiexec -n 8 ipengine --mpi
```

其中`--mpi`参数可以让引擎的rank和MPI的rank一致。这是最基本的使用，当然也可以自定义配置文件，传递给`--profile`参数，实现的东西都是类似的。当然，每次都指定`ipcontroller`的ip地址，以及拷贝`ipycontroller-engine.json`太麻烦了，在linux或者mac里可以指定`alias`把这些过程全部自动化（windows下面应该有对应的东西）：

```shell
# useful variables
export ip=$(ifconfig -a|grep inet|grep -v 127.0.0.1|\
grep -v inet6|awk '{print $2}'|tr -d "addr:")

# alias
alias ipcontroller='ipcontroller --ip='*' --location=${ip}'
alias ipengines="scp ~/.ipython/profile_default/security/ipcontroller-engine.json \
your_host@xxx.xxx.xx.xxx:C:/Users/your_host/.ipython/profile_default/security && \
ssh your_host@xxx.xxx.xx.xxx \
'cd your_work_dir && \
mpiexec -n 8 ipengine --mpi'"
```

在mac里，可以在环境变量中添加当前的ip地址，然后通过`alias`指定在执行`ipengines`命令时先把生成的`ipycontroller-engine.json`直接用scp传递到远程主机上，然后在远程主机的工作目录下启动引擎。在windows上可以安装OpenSSH 服务器来使得可以像用ssh连接linux服务器一样连接windows主机，这里的`your_host`就是windows主机上用户名，后面是ip地址，`your_work_dir`是启动引擎的工作目录。工作目录中需要包含要运行的文件。为了使得在controller端修改文件后win上也能同步修改，比较方便的处理办法是把工作目录设置成坚果云的同步文件夹，这样就实现了文件共享。

运行`ipcontroller`和`ipengines`：

![image-20210526103007563](/Users/santashen/Library/Application Support/typora-user-images/image-20210526103007563.png)

成功连接。上面是在tumx里一个会话分隔出的两个窗格，tumx可以解绑会话与窗口，关掉后仍能在后台继续保持运行。想要关闭控制器和引擎时，运行`tmux kill-session -t xxx`即可。

## numba+ipyparallel+mpi4py

python由于GIL的存在，本身无法实现多线程的并行计算，写多线程的话可能需要cython或者pybind等写一些C或者C++的程序。目前我自己觉得纯python比较方便实现相对较高的计算效率的方式就是结合numba和mpi4py，串行部分用numba完成，在原始程序外包装一个`run.py`的mpi4py运行接口，开出多个进程做并行化，以一个简单的向量求和为例，定义一个`sum.py`文件：

```python
from mpi4py import MPI
import numpy as np
import numba as nb

@nb.jit(nopython=True)
def nb_sum(x):
    sum = 0
    for i in x:
        sum += i
    return sum

def psum(x):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    if rank==0:
        data = np.array_split(x,size)
    else:
        data = None

    data = comm.scatter(data,root=0)
    local_sum = nb_sum(data)
    all_sum = comm.reduce(local_sum,root=0,op=MPI.SUM)

    if rank==0:
        return all_sum
    else:
        return rank
```

其中局部求和函数用numba做优化，psum作mpi调度，在ipython中，运行如下命令：

```python
import numpy as np
import ipyparallel as ipp

c = ipp.Client()
view = c[:]
view.activate()
view.run('sum.py')

view['x'] = np.arange(0,80,dtype='float')

%px sum = psum(x)

view['sum']
```

其中用`%px`魔法命令运行函数调用，用`view.activate`指定`%px`代表的是view，view先运行`sum.py`，让所有引擎都运行`sum.py`，都具有函数信息，用`view['x']`给所有的进程赋值x，最终输出为：

```python
[3160.0, 1, 2, 3, 4, 5, 6, 7]
```









