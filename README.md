tk-maya-playblast
=================

A simple play blast app for Shotgun Toolkit

Add to your shot env file like this:

```
tk-maya-playblast:
    current_scene_template: maya_shot_work
    height: 1080
    location: {path: 'https://github.com/mfx-cgi/tk-maya-playblast.git',
        type: git, version: v0.0.1}
    playblast_template: maya_shot_playblast
    width: 1920
```

Template examples:

```
maya_shot_playblast: '@shot_root/work/images/{pipe_step}[_{name}]/v{version}/{Shot}_{pipe_step}[_{name}].v{version}'
```
