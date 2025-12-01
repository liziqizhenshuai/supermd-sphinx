---
id: configure
title: "配置文件"
sidebar_label: "配置文件"
---

superMD 从 v0.4.0 开始，使用 [yaml](https://yaml.org) 格式开始作为配置文件的格式（v0.2.0 和 v0.3.x 使用 [toml](https://github.com/toml-lang/toml) 格式)。

## 1.示例

以下展示了 superMD 配置文件的部分示例：
```yaml
# <a href='https://yaml.org'>yaml</a> configure file for superMD application,
# writen by <a href='mailto:genshenchu@gmail.com'>genshen</a>"

title: "superMD Configure File"
version: "0.4.0"
contributors:
  original_author: "BaiHe"
  original_author_email: "baihe_ustb@163.com"
  developers: ["BaiHe<baihe_ustb@163.com>", "ChuGenshen<genshenchu@gmail.com>"]
  organization: "USTB"

simulation:
  phasespace: [50, 50, 50]
  cutoff_radius_factor: 1.96125
  lattice_const: 2.85532
  def_timesteps_length: 0.001

potential:
  type: "setfl"
  file_path: "FeCuNi.eam.alloy"

creation:
  create_phase: true
  create_seed: 466953
  create_t_set: 600
  alloy:
    create_seed: 1024
    types:
      - name: Fe
        mass: 55.845
        weight: 97
      - name: Cu
        mass: 63.546
        weight: 2
      - name: Ni
        mass: 58.6934
        weight: 1

output:
  atom_dump:
    presets:
      - name: my_dump
        region: [ 25.0, 25.0, 25.0, 80.4, 80.4, 80.4 ]
        mode: "copy"
        file_path: "supermd_mdl.{}.out"
        by_frame: true
      - name: collision_dump
        mode: "copy"
        file_path: "before_collision.{}.out"
        by_frame: true
  thermo:
    interval: 0
  logs:
    logs_mode: "console"
    logs_filename: ""

stages:
  - name: rescale
    step_length: 0.001
    steps: 4
    dump:
      use: my_dump
      every_steps: 2
    rescale:
      t: 600
      every_steps: 2

  - name: collision
    step_length: 0.0001
    steps: 8
    dump:
      use: collision_dump
      every_steps: 1
    set_v:
      collision_step: 2
      lat: [2, 2, 2, 0]
      energy: 6.8
      direction: [1.0, 1.0, 1.0]

  - name: run
    step_length: 0.001
    steps: 6
```

## 2.使用配置文件
你可以在运行 superMD 程序时，通过命令行参数指定配置文件路径，程序能够读取配置文件，以进行后续模拟，例如：

```bash
mpirun -n 4 /path/of/supermd  -c /path/of/config.yaml
```
或者：

```bash
mpirun -n 4 /path/of/supermd  --conf=/path/of/config.yaml
```
