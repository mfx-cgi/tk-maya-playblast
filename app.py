# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

"""
A breakdown app which shows what in the scene is out of date.

"""

import os

from tank.platform import Application
import tank

import pymel.core as pm


class MayaPlayblast(Application):

    def init_app(self):
        if self.context.entity is None:
            raise tank.TankError("Cannot load the Playblast application! "
                                 "Your current context does not have an entity (e.g. "
                                 "a current Shot, current Asset etc). This app requires "
                                 "an entity as part of the context in order to work.")

        self._playblast_template = self.get_template("playblast_template")
        self._scene_template = self.get_template("current_scene_template")

        self.engine.register_command("Playblast", self.run_app)

    def destroy_app(self):
        self.log_debug("Destroying sg_set_frame_range")

    def run_app(self):
        """
        Callback from when the menu is clicked.
        """
        width = self.get_setting("width", 1920)
        height = self.get_setting("height", 1080)
        start_frame = pm.animation.playbackOptions(query=True, minTime=True)
        end_frame = pm.animation.playbackOptions(query=True, maxTime=True)

        # now try to see if we are in a normal work file
        # in that case deduce the name from it
        curr_filename = os.path.abspath(pm.system.sceneName())
        version = 0
        name = ""
        if self._scene_template.validate(curr_filename):
            fields = self._scene_template.get_fields(curr_filename)
            name = fields.get("name")
            version = fields.get("version")

        fields = self.context.as_template_fields(self._playblast_template)
        if name:
            fields["name"] = name
        if version is not None:
            fields["version"] = version

        playblast_path = self._playblast_template.apply_fields(fields)

        # Save display states
        sel_nurbs_curves = pm.windows.modelEditor('modelPanel4', query=True, nurbsCurves=True)
        sel_locators = pm.windows.modelEditor('modelPanel4', query=True, locators=True)
        sel_joints = pm.windows.modelEditor('modelPanel4', query=True, joints=True)
        sel_ik = pm.windows.modelEditor('modelPanel4', query=True, ikHandles=True)
        sel_deformers = pm.windows.modelEditor('modelPanel4', query=True, deformers=True)
        sel_grid = pm.windows.modelEditor('modelPanel4', query=True, grid=True)

        # Set display states
        pm.windows.modelEditor('modelPanel4', edit=True, nurbsCurves=False)
        pm.windows.modelEditor('modelPanel4', edit=True, locators=False)
        pm.windows.modelEditor('modelPanel4', edit=True, joints=False)
        pm.windows.modelEditor('modelPanel4', edit=True, ikHandles=False)
        pm.windows.modelEditor('modelPanel4', edit=True, deformers=False)
        pm.windows.modelEditor('modelPanel4', edit=True, grid=False)

        pm.animation.playblast(
            filename=playblast_path, format='iff', compression='png',
            width=width, height=height, percent=100,
            showOrnaments=False, viewer=True,
            sequenceTime=False, framePadding=4, clearCache=True)

        # Reset display states
        pm.windows.modelEditor('modelPanel4', edit=True, nurbsCurves=sel_nurbs_curves)
        pm.windows.modelEditor('modelPanel4', edit=True, locators=sel_locators)
        pm.windows.modelEditor('modelPanel4', edit=True, joints=sel_joints)
        pm.windows.modelEditor('modelPanel4', edit=True, ikHandles=sel_ik)
        pm.windows.modelEditor('modelPanel4', edit=True, deformers=sel_deformers)
        pm.windows.modelEditor('modelPanel4', edit=True, grid=sel_grid)
