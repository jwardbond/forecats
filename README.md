Forecats
=========
Wake up every morning (more) excited to look at the forecast! This is a custom Home Assistant integration which uses forecast data, pictures of your pets, and Google's Nano Banana API to generate and serve weather-themed drawings of your precious babies every morning. 

Blog post [here](https://secondthoughts.my/posts/projects/forecats/).

![A picture of two cats and a snowy, cloudy forecast combine to make a drawing of two cats in scarves looking out a window](static/img/diagram.png)

**Features**
- Home assistant integration to generate pictures
- Customizable automation template to control drawing styles, generation times, etc.
- Optional optimization for E-ink screens (currently limited to spectra6 panels)

## Examples

You can display it on an e-ink screen

<img src="static/img/e-ink-screen.jpg" alt="A cat in front of an e-ink screen" width="400">

Or on your HA Dashboard

<img src="static/img/screenshot.png" alt="Home Assistant app screenshot" width="400">


Works in better weather

<img src="static/img/example4.png" alt="Two cats with sunglasses" width="400">

## Getting Started
> [!WARNING]
> This will cost money. You get (I think) $300 of Gemini credits upon sign up, but eventually you will have to pay ~$0.14 every time this runs.

### Requirements
- A [home assistant server](https://www.home-assistant.io/installation/) with the following add-ons
  - [File editor add-on](https://www.home-assistant.io/common-tasks/os/#installing-and-using-the-file-editor-add-on)
  - [Terminal and ssh add-on](https://www.home-assistant.io/common-tasks/os/#installing-and-using-the-ssh-add-on)
  - [Meteorologisk institutt (Met.no)](https://www.home-assistant.io/integrations/met/) integration
- A google AI studio [API key](https://aistudio.google.com/api-keys). Note that, as of writing, you need to input billing details to get the free credits.

### Setup

#### Option A: Install via HACS (recommended)

1. Install [HACS](https://hacs.xyz/) if you haven't already.
2. In HACS, click **Custom repositories** and add `https://github.com/jwardbond/forecats` with category **Integration**.
3. Search for "Daily Forecats" in HACS and install it.
4. Restart Home Assistant, then continue from step 2 below.

#### Option B: Manual install

*Do the following in your HA server, using the Terminal & SSH addon, or `docker exec` if you are running a container on a host system*

1. **Create the necessary directory structure** in your Home Assistant server:

  ```bash
  mkdir -p /config/custom_components && mkdir -p /config/forecats_data/input_images
  ```

2. **Download and copy the integration files**

  ```bash
  cd /tmp && git clone https://github.com/jwardbond/forecats.git && cp -r forecats/custom_components/forecats /config/custom_components/
  ```

---

2. **Select and upload cat images**
  - Choose good pictures of your pets.
  - Rename the files so the pets' names are in the filenames.
  - Upload them to `/config/forecats_data/input_images`.

3. **Enable the custom integration** by adding `forecats:` to your configuration file:

  ```yaml
  # configuration.yaml

  default_config:

  # ...existing data

  automation: !include automations.yaml

  forecats:
  ```

5. **Set up the automation** using one of the following options:

  **Option A: Blueprint (recommended)**
  - Go to **Settings > Automations & Scenes > Blueprints** and click **Import Blueprint**.
  - Paste the URL: `https://github.com/jwardbond/forecats/blob/master/blueprints/automation/forecats/forecats.yaml`
  - Create an automation from the blueprint and fill in your details.

  **Option B: Manual**
  - Copy the [automation template](config_examples/automation_fragment.yaml) into `config/automations.yaml`.
  - Fill out or remove any `<>` placeholders.

6. **Restart your server**

**That's it!** Every morning at 5:00 am, the forecats integration will generate the following images in the `config/www/daily_forecats/` directory:
- `forecats_original.png`: the unprocessed output image from Gemini
- `forecats_optimized.png`: the output image cropped to your desired size and adjusted for display on your screen (currently only supports color adjustments for Spectra6 e-ink)

These images should be accessible on your local network at (e.g.): `<YOUR HA URL>/local/daily_forecats/forecats_original.png`

>[!Note]
> It takes 10-30 seconds for gemini to generate the image. If you have any automations grabbing the image, then I recommend setting them to run a minute after the `generate forecats` autmation is set to run.

> [!Note]
> To test the automation, go to `developer tools > actions > generate forecats` and run it manually.




## Local Testing
I got annoyed testing out new prompts on HA, so I made a folder to experiment locally. If you would like to use it:

1. Clone the repo and enter the testing folder:
  ```bash
  git clone https://github.com/jwardbond/forecats.git && cd forecats/local_testing
  ```
1. Add your cat images to the `forecats_data/input_images` folder.
2. Create a `.env` file with your Gemini API key.
3. Copy the data from your automation into `test.py`.
4. Run:
  ```bash
  uv run test.py
  ```

## (Optional) Sending to an e-ink screen
You will need a screen controllable with ESPHOME. I used seeed studio's [e10002 spectra6 display](https://www.seeedstudio.com/reTerminal-E1002-p-6533.html). I've included the esphome config I use [here](https://github.com/jwardbond/forecats/blob/ha_integration/config_examples/seeede1002.yaml). The basic idea is to set the automation to run every day at a 5:00 am, and have the screen wake up every day slightly before that, download the picture at 5:01 am (to leave time to generate), and then go into deep sleep until the next day.


## TODO
- [x] Enrol in HACS for easier install
- [ ] Option to save images to dir
- [x] Make automation into blueprint for easier install
- [ ] Separate e-ink instructions
- [ ] See if I can make it more configurable from GUI
- [ ] Support for multiple cities