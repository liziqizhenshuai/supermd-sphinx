---
id: configure-terms
title: "配置项说明"
sidebar_label: "配置项说明"
---

配置文件的示例见`$MD_PATH/example/config.yaml`, 其中配置文件的各个字段如下，你可以根据你的需求修改各选项的值。

## 基本配置
基本配置指定模拟的基本信息，如空间信息(晶格点数、截断半径等)，体系创建等配置。

### simulation
说明：指定模拟的基本信息，如box大小、截断半径等;

### simulation.phasespace
类型: Integer 数组, 长度: 3;  
说明：模拟盒子大小，分别为x、y、z三个维度上的尺寸；单位为晶格常数;

### simulation.lattice_const
类型: Float;  
单位: 埃, Å;  
说明: 晶格常数;

### simulation.cutoff_radius_factor
类型: Float;  
说明: 截断半径系数; 截断半径系数乘以晶格常数等于实际的截断半径长度;

### simulation.def_timesteps_length
类型：Float;  
单位：皮秒, ps;  
说明：模拟中默认的每一个时间步长度;  

### creation
说明：指定模拟初始化时创建模拟体系的相关参数;

### creation.create_phase
类型：Boolean;  
说明：true表示程序初始化时，按照给定参数(如温度)随机创建原子；false表示读入已有的原子信息以创建原子;  

### creation.create_seed
类型：Integer;  
说明：创建原子信息的随机数种子；仅 `creation.create_phase` 为 true 时有效;  

### creation.create_t_set
类型：Float;  
说明：创建的体系的温度；仅 `creation.create_phase` 为 true 时有效;  

### creation.alloy
说明：合金元素的相关配置; 该部分仅 `creation.create_phase` 为 true 时有效;  

### creation.alloy.create_seed
类型：Integer;  
说明：创建原子时，随机生成不同种类合金原子的随机数种子;  

### creation.alloy.types
说明：合金元素的相关类型配置，可以指定模拟体系中合金的相关名称、相对原子质量及比例;  

### creation.alloy.types.name
类型：String;  
说明：合金名称，用户自定义字符串，一般可以用化学式符号;  

### creation.alloy.types.mass
类型：Float;  
说明：合金对应元素的相对原子质量;  

### creation.alloy.types.weight
类型：Integer;  
说明：合金中该元素的权重，用于指定在创建体系时，随机生成的各类合金原子的比例;  

### potential
说明：势函数文件相关参数;  

### potential.type
类型：String  
说明：势函数文件格式, 取值"setfl"或者"funcfl"，目前仅支持 setfl 格式;  

### potential.file_path
类型：String  
说明：势函数文件路径;  

### output
说明：输出相关配置;

### output.atom_dump.presets
说明：预设的体系 dump 配置，包括 dump 文件名、输出模拟等配置，在 stage 中可使用这些预设的 dump 配置。

### output.atom_dump.presets.name
类型：String  
说明：预设的 dump 配置的名称，在 stage 中可通过该名称使用对应的预设 dump 配置;

### output.atom_dump.presets.region
类型：Float 数组，长度: 6;  
单位: 埃, Å;  
说明：输出指定区域的粒子信息，该数组指定区域的开始和结束坐标. 
该参数是可选的，如果不指定，则默认输出模拟体系中所有的粒子信息;

### output.atom_dump.presets.mode
说明：输出模式，取值为"copy"或者"direct"；copy模式输出一个文件，二进制格式;  
direct模式输出多个文本文件(每个进程与每一个需要输出的时间步都对应一个文件)，一般用于程序调试;

### output.atom_dump.presets.file_path
类型：String  
说明：copy模式下，输出二进制文件路径;
如果设置了按帧输出(`output.by_frame`为true), 则文件路径中需要有一个大括号(如`misa_mdl.{}.out`),程序输出时会将大括号替换为当前时间步数.  

### output.atom_dump.presets.by_frame
类型: Boolean  
说明: 每隔指定的时间步数输出一次体系的粒子信息（在 stage 中配置）为一帧。
如果此按帧输出选项打开，程序会在每一帧时创建一个输出文件，否则将会将所有的帧都写入到一个文件中。

### output.thermo
说明：热力学信息的输出相关配置;

### output.thermo.interval
类型：Integer  
说明：指定每隔一定时间步输出系统的热力学信息，包括体系温度、能量等; 

### output.logs
说明：程序日志, 可以选择输出到标准输出或者文件.

### output.logs.logs_mode
类型：String  
说明：日志输出模式,可以为`console`(输出到标准输出)或者`file`(输出到文件).

### output.logs.logs_filename
类型：String  
说明：如果日志输出模式为file, 该选项指定文件路径.

## STAGES
stage允许一个模拟流程可以分为若干个stages，借鉴自 gitlab-ci 和 github action。每个 stage 中依据该stage的配置参数执行若干时间步。  
目前 stage 中可以配置时间步、时间步长等参数以及rescale、PKA级联碰撞等操作。

### [stage].name
类型：String  
说明：stage 名称;

### [stage].steps
类型：Integer  
说明：该 stage 执行的模拟时间步数;

### [stage].step_length
类型：Float  
单位：皮秒, ps;  
说明：该 stage 执行的模拟所使用的时间步长，如不指定则使用默认时间步长(由`simulation.def_timesteps_length`指定);

### [stage].rescale
说明：每隔一定时间步进行一次rescale，将体系温度重新设置为给定的温度; 该选项指定rescale 的相关参数;  

### [stage].rescale.t
类型：Float;  
单位：开, K;  
说明：每次rescale时，重新设置的体系温度;

### [stage].rescale.every_steps
类型：Integer  
说明：执行 rescale 操作的时间步间隔; 

### [stage].setv
说明：级联碰撞的相关参数;  

### [stage].setv.collision_step
类型：Integer;  
说明：指定级联碰撞开始的时间步，该时间步时相对于该stage的，而非全局时间步;  

### [stage].setv.lat
类型：Integer 数组，长度: 4;  
说明：级联碰撞PKA原子位置，数组第4项为偏移值，一般设为0;  

### [stage].setv.energy
类型：Float  
说明：用于设置级联碰撞PKA原子能量，单位eV，直接叠加到对应原子的速度上; 

### [stage].setv.direction
类型：Integer 数组，长度: 3;  
说明：用于设置PKA能量对应的速度在三个维度(x,y,z)的分量，或者说是PKA入射方向; 

### [stage].dump
说明：dump 体系粒子信息的相关参数配置; 
需要说明的是，dump 配置仅针对当前的 stage 生效，即作用域仅限制在本 stage，
如果需要在其他 stage 中输出体系粒子信息，需要在其他 stage 中配置对应的 `dump`。

### [stage].dump.use
类型：String  
说明：引用的 dump preset 的名称，采用该 preset 中的配置（如文件名、输出区域等）进行体系粒子的输出;

### [stage].dump.every_steps
类型：Integer  
说明：每间隔该项指定的时间步数，输出一帧体系中的粒子信息.
