'''
Python tool for generating a static map given an adress or coordinate.
'''

import sys
import logging
import argparse
import staticmap
import geocoder

# https://wiki.openstreetmap.org/wiki/Tile_servers
URL_TEMPLATES = {
  "ThunderforestLandscape":"http://tile.thunderforest.com/landscape/{z}/{x}/{y}.png",
  "ThunderforestOutdoors":"  http://tile.thunderforest.com/outdoors/{z}/{x}/{y}.png",
  "Watercolor":"http://c.tile.stamen.com/watercolor/{z}/{x}/{y}.jpg",
  "Toner":"http://a.tile.stamen.com/toner/{z}/{x}/{y}.png",
  "OSM":"https://a.tile.openstreetmap.org/{z}/{x}/{y}.png",
  "Hillshade":"http://c.tiles.wmflabs.org/hillshading/{z}/{x}/{y}.png",
  "Humanitarian":"http://a.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png ",
}

DEFAULT_TEMPLATE = "OSM"

def georeference(place):
  location = geocoder.arcgis(place)
  return location[0]


def generateMap(
  latitude, 
  longitude, 
  dest_file, 
  zoom=12,
  width=640, 
  height=480, 
  template=DEFAULT_TEMPLATE):
  
  coord = (longitude, latitude)
  m = staticmap.StaticMap(width, height, 10, url_template=URL_TEMPLATES[template])
  marker_outline = staticmap.CircleMarker(coord, "white", 18)
  marker = staticmap.CircleMarker(coord, "#0036FF", 10)
  m.add_marker(marker_outline)
  m.add_marker(marker)
  image = m.render(zoom=zoom)
  image.save(dest_file)


def main():
  parser = argparse.ArgumentParser(description='Generate a static map for address or location')
  parser.add_argument(
    '-l', '--log_level',
    action='count',
    default=0,
    help='Set logging level, multiples for more detailed.')
  parser.add_argument(
    '-o','--outfile',
    default='map.png',
    help='Name of generated map file.')
  parser.add_argument(
    '-T','--latitude',
    default=None,
    help='Latitude in decimal degrees (overrides address).')
  parser.add_argument(
    '-G','--longitude',
    default=None,
    help='Longitude in decimal degrees (overrides address).')
  parser.add_argument(
    '-C','--coordinate',
    default=None,
    help='Latitude,Longitude in decimal degrees (overrides address).')
  parser.add_argument(
    '-z','--zoom',
    default=12,
    help='Zoom factor (1-14)')
  parser.add_argument(
    '-W','--width',
    default=640,
    help='Width of generated image.')
  parser.add_argument(
    '-H','--height',
    default=480,
    help='Height of generated image.')
  parser.add_argument(
    '-t','--template',
    default=DEFAULT_TEMPLATE,
    help='Name of template to use.')
  parser.add_argument(
    'address', 
    default=None,
    nargs='?',
    help='Address of location to show.')
  args = parser.parse_args()
  # Setup logging verbosity
  levels = [logging.WARNING, logging.INFO, logging.DEBUG]
  level = levels[min(len(levels) - 1, args.log_level)]
  logging.basicConfig(level=level,
                      format="%(asctime)s %(levelname)s %(message)s")

  template = args.template
  if not template in URL_TEMPLATES:
    logging.error("Template %s is not available.", template)
    logging.info("Available templates include: %s", "\n".join(URL_TEMPLATES.keys()))
    return 0
  coordinates = {'latitude':None, 'longitude':None}
  if args.coordinate is not None:
    coords = [float(c.strip()) for c in args.coordinates.split(',')]
    coordinates['latitude'] = coords[0]
    coordinates['longitude'] = coords[1]
  else:
    if args.latitude is not None:
      coordinates['latitude'] = float(args.latitude.strip())
    if args.longitude is not None:
      coordinates['longitude'] = float(args.longitude.strip())
  if coordinates['latitude'] is None or coordiantes['longitude'] is None:
    if args.address is None:
      logging.error("Address or cordinates are required.")
      return(1)
    location = georeference(args.address)
    coordinates['latitude'] = location.lat
    coordinates['longitude'] = location.lng
  zoom = int(args.zoom)
  width = int(args.width)
  height = int(args.height)
  dest_file = args.outfile
  generateMap(
    coordinates['latitude'],
    coordinates['longitude'],
    dest_file,
    zoom=zoom,
    width=width,
    height=height)

if __name__ == "__main__":
  sys.exit(main())

