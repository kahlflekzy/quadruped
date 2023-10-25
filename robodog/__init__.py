import os
import time

import mujoco.viewer

if __name__ == "__main__":
    cwd = os.getcwd()
    model = mujoco.MjModel.from_xml_path(filename=f'{cwd}/robodog/model/scene.xml', assets=None)

    data = mujoco.MjData(model)
    copy = data.qpos.copy()
    mujoco.mj_kinematics(model, data)

    ctx = mujoco.GLContext(2000, 2000)
    ctx.make_current()

    with mujoco.viewer.launch_passive(model, data) as viewer:
        start = time.time()
        mujoco.mj_step(model, data)
        while viewer.is_running():
            step_start = time.time()

            data.qpos = copy.copy()
            mujoco.mj_step(model, data)
            mujoco.mj_kinematics(model, data)

            with viewer.lock():
                viewer.opt.flags[mujoco.mjtVisFlag.mjVIS_CONTACTPOINT] = int(data.time % 2)

            viewer.sync()
            time_until_next_step = model.opt.timestep - (time.time() - step_start)
            if time_until_next_step > 0:
                time.sleep(time_until_next_step)
