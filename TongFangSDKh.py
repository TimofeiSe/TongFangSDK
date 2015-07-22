#!/usr/sbin/env python
# -*- coding: utf-8 -*-

# import ctypes
# from TongFangSDKdefines import *
# from TongFangSDKstructs import *
from TongFangSDKfunctns import *


if __name__ == '__main__':
	from time import sleep
	try:
		
		tfc_Init()
		
		user_id, info = tfc_Login('172.20.23.67')
		print 'Camera {0.name} type {0.device_type}\n\t{0.ipaddr}, mac {0.macaddr}\n\tSn {0.serial}, ver {0.version}\n'.format(info)
		
		print 'user_id =', user_id
		print 
		
		ntp_config = tfc_GetConfig(user_id, CMD_GET_NTP)
		print 'NTP: timeZone =', ntp_config.timeZone
		
		status = tfc_GetConfig(user_id, CMD_GET_DEVICESTATUS)
		print 'Status: iDeviceUpTime =', status.iDeviceUpTime
		
		time_config = tfc_GetConfig(user_id, CMD_GET_TIME)
		print 'Time: Year =', hex(time_config.Year)
		
		mjpeg_config = tfc_GetConfig(user_id, CMD_GET_MJPEGCFG)
		print 'MJPEG: imgQuality =', mjpeg_config.imgQuality
		print 'MJPEG: imgframerate =', mjpeg_config.imgframerate
		
		camera_config = tfc_GetConfig(user_id, CMD_GET_CAMERACFG)
		print 'Camera: day/night =', camera_config.daynight
		print 'Camera: brightness =', camera_config.brightness
		camera_config.brightness = 50
		tfc_SetConfig(user_id, CMD_SET_CAMERACFG, camera_config)
		
		osd_config = tfc_GetConfig(user_id, CMD_GET_OSDCFG)
		print 'OSD: fontsize =', osd_config.fontsize
		print 'OSD: showdate =', osd_config.showdate
		print 'OSD: showtext =', osd_config.showtext
		print 'OSD: textxy =', osd_config.textxy
		print 'OSD: position =', osd_config.position
		osd_config.showdate = osd_config.showtime = osd_config.showinfo = False
		osd_config.showtext = True
		osd_config.text = 'Unfortunately this only works on Windows'
		osd_config.position = 4
		osd_config.textxy = 400, 400
		osd_config.fontsize = 1
		tfc_SetConfig(user_id, CMD_SET_OSDCFG, osd_config)
		
		net_config = tfc_GetConfig(user_id, CMD_GET_NETCFG)
		for iface in net_config.interfaces:
			print 'Net: id =', iface.id
			print 'Net: mac =', iface.mac
			print 'Net: dhcp =', iface.dhcp
			print 'Net: ipaddr =', iface.ipaddr
			print 'Net: ipmask =', iface.ipmask
			print 'Net: ipgateway =', iface.ipgateway
			print 'Net: dns =', iface.dns
			print 'Net: wifi =', iface.wifi.enabled
			print 'Net: status =', iface.status
			print
			iface.ipgateway = '172.20.23.1'
			net_config.interfaces = iface
			print 'Net: ipgateway =', iface.ipgateway

		tfc_SetConfig(user_id, CMD_SET_NETCFG, net_config)
		print 
		net_config2 = tfc_GetConfig(user_id, CMD_GET_NETCFG)
		for iface in net_config2.interfaces:
			print 'Net: ipgateway =', iface.ipgateway
		
		
		tfc_Logout(user_id)
	
		tfc_Cleanup()
		
		
		
		
		
	except Exception, err:
		print err
	finally:
		print 
