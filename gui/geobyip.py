import pygeoip
GEOIP = pygeoip.GeoIP("GeoLiteCity.dat", pygeoip.MEMORY_CACHE)
print GEOIP.time_zone_by_addr("81.218.206.58")