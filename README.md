# chaosview
A simple python program to visualise chaotic flows.

*Mac Instructions*

Note: python 3 must be installed to run the application. The packages required by the app are numpy, PIL, imageio.
To run the app, open the terminal and navigate to the folder with the pyhon file (chaos-sim.py) via the cd command,
e.g. if the file is in Documents, enter 'cd Documents'.
Enter 'python3 chaos-sim.py' to run.
A chaos-sim.app, that can simply be double-clicked to run and doesn't require python installed, will be available in a near-future release.

*App Guidance*

  The intention of this program is to provide a visual demonstration of chaotic advection. The user can fill a region with points and watch them be distorted and form fractal patterns by the action of an alternating shear sine flow. Paramaters such as magnitude of flow velocity and colour of points may be changed. Compound shapes can be created by selecting multiple regions, although this can make the program slow if too many points are added. (the number of points per region, 500 by deafult, is stored by the variable 'n' in the source code if altering it is desirable.)
  
  The 'Reset' button reverts the system to its initial conditions, based on the regions selected by the user. Note that if a region was created after the simulation started playing, it will be reset as if it were created at the start regardless.
 The zero button has a similar but not identical function. It will evolve the system back to the initial condition, rather than simply resetting it. This is useful in demonstrating how sensitive the system is to small changes in initial conditions. For example, with the flow amplitude at the maximum setting, once time as passed around ten seconds pressing zero won't successfully re-create the initial conditions, demonstrating how unpredictable a chaotic system becomes when sufficient time has passed. Note that there is a correlation between flow amplitude and how chaotic the system is - on the lowest setting, initial conditions are successfully recreated by pressing zero even after several hundred seconds.
 
  The clear button effectively erases all progress made, allowing the user to define a completely new set of regions. There is no warning if this occurs, so an interesting flow pattern can easily be lost if the button is pressed by accident.
  The user has the options of either saving an image of the current flow window or saving an animation over several frames. By pressing 'Create Animation', frames will beging to be added to a gif file. Note that frames are added based on updating the frame in the app, so staying on one view longer doesn't mean it will be displayed for longer in the animation. The user can then press 'End Animation' to save the gif.
  
  It is also possible to save an interesting system, close the app, then reload the system when the app is opened again. Upon pressing 'Quit', a prompt will ask the user if they wish to save progress. Choosing 'Yes' then saves a .pickle file, which can be selected via the 'Load' button to restore the system from when the file was created.
  
  There is also a small 'help' button. This is a prototype and has no functionality in this version.
