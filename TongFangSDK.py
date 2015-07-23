#!/usr/sbin/env python
# -*- coding: utf-8 -*-

import time, copy, gc

from TongFangSDKh import *


def TFSdk_Init():
	try:
		tfc_Init()
		return 'success'
	except TongFangSdkError, err:
		return str(err)
	
def TFSdk_Cleanup():
	try:
		tfc_Cleanup()
		return 'success'
	except TongFangSdkError, err:
		return str(err)

def TFSdk_SetOSD(text='timofei@timse.ru', is_show=True, position=None, ip='192.168.1.188', port=1115, username='admin', password='admin'):
	try:
		user_id, device = tfc_Login(ip=ip, port=port, username=username, password=password)
		osd_config = tfc_GetConfig(user_id, CMD_GET_OSDCFG)
		osd_config.position = position if position else osd_config.position
		osd_config.showtext = is_show
		osd_config.text = text
		tfc_SetConfig(user_id, CMD_SET_OSDCFG, osd_config)
		tfc_Logout(user_id)
		result = True
	except TongFangSdkError, err:
		result = 'ERROR: %s' % err
	return result

def TFSdk_SetToUseDHCP(ip='192.168.1.188', port=1115, username='admin', password='admin'):
	try:
		user_id, device = tfc_Login(ip=ip, port=port, username=username, password=password)
		net_config = tfc_GetConfig(user_id, CMD_GET_NETCFG)
		if net_config.interfaces and net_config.interfaces[0].id == 'eth0' and not net_config.interfaces[0].dhcp:
			iface = net_config.interfaces[0]; iface.dhcp = True; net_config.interfaces = iface
			tfc_SetConfig(user_id, CMD_SET_NETCFG, net_config)
			result = 'Set to use DHCP: {0.name} (ip {0.ipaddr}), sn {0.serial}'.format(device)
		else:
			result = 'Already using DHCP: {0.name} (ip {0.ipaddr}), sn {0.serial}'.format(device)
			tfc_Logout(user_id)
	except TongFangSdkError, err:
		result = 'ERROR: %s' % err
	return result
	
def TFSdk_SetToUseStaticIP(ip='192.168.1.188', port=1115, username='admin', password='admin'):
	try:
		user_id, device = tfc_Login(ip=ip, port=port, username=username, password=password)
		net_config = tfc_GetConfig(user_id, CMD_GET_NETCFG)
		if net_config.interfaces and net_config.interfaces[0].id == 'eth0' and net_config.interfaces[0].dhcp:
			iface = net_config.interfaces[0]; iface.dhcp = False; net_config.interfaces = iface
			tongfang_SetConfig(user_id, CMD_SET_NETCFG, net_config)
			result = 'Set to use StaticIP: {0.name} (ip {0.ipaddr}), sn {0.serial}'.format(device)
		else:
			result = 'Already using StaticIP: {0.name} (ip {0.ipaddr}), sn {0.serial}'.format(device)
			tongfang_Logout(user_id)
	except TongFangSdkError, err:
		result = 'ERROR: %s' % err
	return result
	
def TFSdk_SetToUseNewIP(new_ip=None, new_mask=None, new_gw=None, new_dns=None,
			ip='192.168.1.188', port=1115, username='admin', password='admin'):
	try:
		user_id, device = tfc_Login(ip=ip, port=port, username=username, password=password)
		net_config = tfc_GetConfig(user_id, CMD_GET_NETCFG)
		if net_config.interfaces and net_config.interfaces[0].id == 'eth0':
			iface = net_config.interfaces[0]
			if iface.dhcp: iface.dhcp = False
			if new_ip: iface.ipaddr = new_ip
			if new_mask: iface.ipmask = new_mask
			if new_gw: iface.ipgateway = new_gw
			if new_dns: iface.dns = [new_dns, new_dns]
			net_config.interfaces = iface
			tfc_SetConfig(user_id, CMD_SET_NETCFG, net_config)
			result = 'Set to use new StaticIP for: {0.name} (ip {0.ipaddr}), sn {0.serial}'.format(device)
		else:
			result = 'Strange error while trying to use new StaticIP for: {0.name} (ip {0.ipaddr}), sn {0.serial}'.format(device)
	except TongFangSdkError, err:
		result = 'ERROR: %s' % err
	return result
	
	
	
	
	
	
	
search_units_search_id = -1
search_units_searching = False
search_units_counter = 0
search_units_max_repeats = 3
def callback_CameraFound(p_device_info, user_id):
	global search_units_search_id, search_units_searching, search_units_counter, search_units_max_repeats
	try:
		device_info = p_device_info.contents
		if found_cameras.has_key(device_info.serialNum):
			search_units_counter += 1
			if search_units_counter >= search_units_max_repeats:
				search_units_searching = False
				tfc_StopSearchUnits(search_units_search_id)
		else:
			search_units_counter = 0
			print '\t', str(device_info.ip.ipV4)
			found_cameras[device_info.serialNum] = {
					'ip': str(device_info.ip.ipV4), 
					'sn': str(device_info.serialNum), 
					'mac': str(device_info.byMAC), 
					'name': str(device_info.szDeviceName) 
				}
	except ValueError:
		search_units_searching = False
	return
def TFSdk_SearchUnits():
	found_cameras = dict()
	global search_units_search_id, search_units_searching, search_units_counter
	if search_units_searching:
		return 'already searching'
	try:
		tfc_Init()
		user_id = 0
		for local_ip in tfc_GetLocalIP():
			print '---', local_ip
			search_units_search_id = tfc_StartSearchUnits(callback_CameraFound, user_id, local_ip=local_ip)
			search_units_searching = True
			print '--- search_id =', search_units_search_id
			start_time = time.clock()
			prev = ''
			while search_units_searching and time.clock()-start_time < 3:
				now = '%.1f' % (time.clock()-start_time)
				if now != prev: prev = now; print now,
				pass
			print
			if search_units_searching:
				print '---stop =', tfc_StopSearchUnits(search_units_search_id)
				search_units_searching = False
			user_id += 1
	except TFSdkError as err:
		return str(err)
	finally:
		tfc_Cleanup()
	return found_cameras
	
	

class Empty: 
	pass
tfg_searching = False
def TFSdk_SearchUnits2():
	global tfg_searching
	max_time_to_search = 2
	is_show_interface_ip = False
	is_show_time_marks = False
	tfg_searching = False
	found_cameras = dict()
	def fCameraFound(p_device_info, user_id):
		global tfg_searching
		is_show_cameras_found = False
		if tfg_searching and p_device_info:
			device = p_device_info.contents
			if not found_cameras.has_key(device.serial):
				if is_show_cameras_found: print '      camera', device.ipaddr
				found_cameras[device.serial] = copy.deepcopy(device)
			else:
				tfg_searching = False
		else:
			tfg_searching = False
		return
		
	fCameraFoundCB = tfc_fSearchUnitsCB(fCameraFound)
	try:
		tfc_Init(); local_ips = tfc_GetLocalIP(); tfc_Cleanup()
		local_ips.reverse()
		user_id=0
		for local_ip in local_ips:
			tfc_Init()
			if is_show_interface_ip: print 'ip', local_ip
			tfg_searching = True
			search_id = tfc_StartSearchUnits(fCameraFoundCB, user_id, local_ip=local_ip)
			start_time = time.clock()
			prev = '   -.0'
			while tfg_searching and time.clock()-start_time<max_time_to_search:
				current = '   %.1f' % (time.clock()-start_time)
				if is_show_time_marks and prev != current: print prev, tfg_searching; prev = current
				pass
			tfc_StopSearchUnits(search_id)
			tfg_searching = False
			user_id += 1
			tfc_Cleanup()
			
	except TFSdkError as err:
		pass
	return found_cameras

if __name__ == '__main__':
	# gc.set_debug(gc.DEBUG_STATS | gc.DEBUG_COLLECTABLE)
	
	# TFSdk_Init()
	# print TFSdk_SetOSD('Если ваша сеть Ethernet', ip='172.20.23.67')
	# print TFSdk_SetToUseDHCP('172.20.23.67')
	# print TFSdk_SetToUseNewIP('172.20.23.67', ip='172.20.23.68')
	# TFSdk_Cleanup()
	for k, v in TFSdk_SearchUnits2().items():
		print v.device_type, v.name, v.ipaddr, v.macaddr, v.serial, v.version
	print