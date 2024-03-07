# JuliaGUI
A GUI for interactive generation, display and inspection of Julia set images. 



![alt](screenshots/.thumbnails/rabbit1_small.png) ![alt](screenshots/.thumbnails/rabbit2_small.png) ![alt](screenshots/.thumbnails/rabbit3_small.png) 

![alt](screenshots/.thumbnails/dendrite1_small.png) ![alt](screenshots/.thumbnails/dendrite2_small.png) ![alt](screenshots/.thumbnails/dendrite3_small.png) 

![alt](screenshots/.thumbnails/dragon1_small.png) ![alt](screenshots/.thumbnails/dragon2_small.png) ![alt](screenshots/.thumbnails/dragon3_small.png) 


### Installation & Usage

1. **Install Dependencies:**
Ensure you have Python installed on your system. If not, download and install it from [python.org](https://www.python.org/downloads/). Then install the dependencies if you do not already have them.

    - Pillow
    - Numpy

    You can install them manually or with the following command:

    `pip install -r requirements.txt`

2. **Clone the Repository:**

    `git clone https://github.com/spookyboogy/JuliaGUI.git`

3. **Navigate to the Directory:**

    `cd JuliaGUI`

4. **Run the Program:**

    `python juliagui.pyw`

### About Julia sets

Informally speaking, normal Julia sets are defined by the holomorphic equation: 

$$ {\displaystyle f_{c}(z)=z^{2}+c~, \quad c \in \mathbb{C} } $$

Where,

$$  c = a + ib : \quad -2 \leq a \leq 2, \quad -2 \leq b \leq 2, \quad a,b \in \mathbb{R} $$

The Julia set associated with a particular complex number $ c $ 
is the boundary separating the set of points in the complex plane that remain bounded under iteration of the function $ f_{c}(z) $ from those that tend toward infinity.

While those aren't strict ranges for $ a $ and $ b $, most recognizable Julia sets come from values within that range, as they tend to correspond to connected Julia sets. When a Julia set is connected, it implies a higher degree of stability in the behavior of the iterated function $ f_{c}(z) $.

The [Mandelbrot set](https://en.wikipedia.org/wiki/Mandelbrot_set) acts as a parameter space for or an index of Julia sets. Each point in the Mandelbrot set corresponds to a different Julia set. If a point in the Mandelbrot set corresponds to a connected Julia set, then the Julia set is said to be in the Mandelbrot set.

To learn more about these fascinating mathematical objects, check out the [Julia set wikipedia page](https://en.wikipedia.org/wiki/Julia_set) :)


### Using the control panel

![alt](screenshots/control_panel.png)

- Redraw : After setting new value(s) for a and b, this triggers a redraw of the julia set. If a and b are unchanged, this returns to the original zoom level
- Resize : By default, images are rendered at 500px x 500px resolution. The resize button allows you to increase or decrease the resolution to your liking. Note that larger resolutions take longer to render.
- Zoombox : Select a rectangular region on the canvas to zoom into
- Safe(r)zoom : Select a (strictly) square region to zoom into. More stable/consistent than zoombox.
- <--- : Go to the previously genereated image, ie a lesser level of zoom
- ---> : Go to the next image, higher level of zoom, if it exists
- Random : Selects random values for a and b and triggers a redraw
- Export : Export the current image to a format other than .pgm  


<details>
<summary> </summary>

<script
  src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"
  type="text/javascript">
</script>

</details>