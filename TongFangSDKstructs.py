#!/usr/sbin/env python
# -*- coding: utf-8 -*-

import ctypes
from TongFangSDKdefines import *

#--- ENUMS --------------------------------------------------------------------------------------------------
'''
eOperateType, enumOperateType:
	OPERATE_ADD_USER    = 0x0,
	OPERATE_MODIFY_USER = 0x1,
	OPERATE_DELETE_USER = 0x2

eSetPara, enumSetPara:
	SET_PARA_NONE      = 0x0,
	SET_PARA_MEM       = 0x1,  /// Set Parameter to memory
	SET_PARA_INI       = 0x2   /// Set Parameter to ini file

eGetPara, enumGetPara:
	GET_PARA_NONE      = 0x0,
	GET_PARA_MEM       = 0x1,  /// Set Parameter to memory
	GET_PARA_INI       = 0x2   /// Set Parameter to ini file

eRecordType, enumRecordType:
	ALARM_RECORD = 0,
	SCHE_RECORD,
	MANUAL_RECORD, 
	ALL_RECORD,
	RECORD_BUTT,

eFileFormat, enumFileFormat:
	FILE_FORMAT_AVI,
	FILE_FORMAT_MP4,
	FILE_FORMAT_ALL,
	FILE_FORMAT_BUTT,
'''



#--- STRUCTS -----------------------------------------------------------------------------------------------

class IPAddr_t (cStruct): #< ipver: 1- IPV4, 2- IPV6, 3- IPVDUAL
	_fields_ = [('ipver', INT), ('ipV4', CHAR * IPADRRESS_LEN), ('ipV6', CHAR * IPV6ADDRESS_LEN) ]

class UserLoginInfo_t (cStruct):
	_fields_ = [ ('netType', INT), ('userIPAddr', IPAddr_t), ('szUserName', CHAR * (MAX_USERNAME_LEN + 1)), ('szPassword', CHAR * (MAX_PWD_LEN + 1)), ('port', UINT) ]
	def __init__(self, ip='192.168.1.188', port=1115, username='admin', password='admin'):
		self.netType = 0 #< 0: LAN, 1: WAN, 2: WIFI, 3: 3G
		self.userIPAddr.ipver, self.userIPAddr.ipV4 = 1, ip[:IPADRRESS_LEN]
		self.port, self.szUserName, self.szPassword = port, username[:MAX_USERNAME_LEN], password[:MAX_PWD_LEN]

class DeviceInfo_t (cStruct):
	_fields_ = [('softver', UINT), ('hardver', UINT), ('panelver', UINT), ('devType', UINT), ('serialNum', CHAR * (MAX_SERIAL_NUM + 1)), ('szDeviceName', CHAR * (MAX_DEVICE_NAME_LEN + 1)), ('byMAC', CHAR * (MAC_LEN + 1)), ('ip', IPAddr_t), ('httpPort', UINT), ('ftpPort', UINT), ('rtspPort', UINT), ('tcpPort', UINT), ('updateTimes', UINT), ('alarminNum', CHAR), ('alarmoutNum', CHAR), ('maxChan', CHAR), ('audioChan', CHAR), ('resolution', CHAR), ('wifi', CHAR), ('sdslot', CHAR), ('diskNum', CHAR)]
	@property
	def version(self): return 'S.%d/H.%d/P.%d' % (self.softver, self.hardver, self.panelver)
	@property
	def device_type(self): return self.devType
	@property
	def name(self): return self.szDeviceName
	@property
	def serial(self): return self.serialNum
	@property
	def ipaddr(self): return self.ip.ipV4
	@property
	def macaddr(self): return self.byMAC



class Etherlink_t (cStruct):
	_fields_ = [
		('struIP', IPAddr_t), ('struIPMask', IPAddr_t), ('struGatewayIpAddr', IPAddr_t), ('byMAC', CHAR * (MAC_LEN + 1))
	]
class DNSAddr_t (cStruct):
	_fields_ = [
		('DNS1', IPAddr_t), ('DNS2', IPAddr_t) 
	]
class PPPOECfg_t (cStruct):
	_fields_ = [
		('enable', INT), ('szUserName', CHAR * (MAX_USERNAME_LEN + 1)), ('szPassword', CHAR * (MAX_PWD_LEN + 1)), ('struPPPoEIP', IPAddr_t) 
	]
class NetCfg_t (cStruct):
	_fields_ = [
		('bUseDhcp', INT), ('struEtherNet', Etherlink_t), ('struDNSServer', DNSAddr_t), ('struPPPoE', PPPOECfg_t) 
	]




class WEP_t (cStruct): #< authenticationType: 0 for open, 1 for share, 2 for auto; keyLength: 64 or 128
	_fields_ = [('authenticationType', INT), ('keyIndex', INT), ('keyLength', INT), ('encryption', CHAR * 4 * (MAX_WIFIWEP128KEY_LEN + 1))]
class WPA_t (cStruct): #< algorithm: 0 for TKIP, 1 for AES, 2 for TKIP/AES.
	_fields_ = [('algorithm', INT), ('sharedKey', CHAR * (MAX_WIFIWPAKEY_LEN + 1))]
class WirelessSecurity_t (cStruct): #< mode: 0 for none, 1 for WEP, 2 for WPA, 3 for WPA2.
	_fields_ = [('mode', INT), ('wep', WEP_t), ('wpa', WPA_t) ]
class Wifi_t (cStruct): #< channel: 1-14 and 0 for auto.
	_fields_ = [('enabled', INT), ('wmmEnabled', INT), ('networkType', INT), ('channel', INT), ('ssid', CHAR * (MAX_WIFISSID_LEN + 1)), ('security' ,WirelessSecurity_t), ('struEtherNet', Etherlink_t)]
class PPPoEServer_t (cStruct):
	_fields_ = [('ipAddress', CHAR * IPADDRESS_LEN), ('ipV6Address', CHAR * IPV6ADDRESS_LEN)]
class PPPoEClient_t (cStruct):
	_fields_ = [('ipAddress', CHAR * IPADDRESS_LEN), ('ipV6Address', CHAR * IPV6ADDRESS_LEN)]
class PPPoE_t (cStruct): #< id: pppoe interface identifier.
	_fields_ = [('enabled', INT), ('id', CHAR * 8), ('user', CHAR * (MAX_USERNAME_LEN + 1)), ('password', CHAR * (MAX_PWD_LEN + 1)), ('server', PPPoEServer_t), ('client', PPPoEClient_t)]
class AddressRange_t (cStruct):
	_fields_ = [('startIpAddress', CHAR * IPADDRESS_LEN), ('endIpAddress', CHAR * IPV6ADDRESS_LEN), ('startIpV6Address', CHAR * IPV6ADDRESS_LEN), ('endIpV6Address', CHAR * IPV6ADDRESS_LEN)]
class AddressMask_t (cStruct): #< bitMask: number of '1' of net mask.
	_fields_ = [('ipAddress', CHAR * IPADDRESS_LEN), ('ipV6Address', CHAR * IPV6ADDRESS_LEN), ('bitMask', CHAR * IPV6ADDRESS_LEN)]
class IPFilterAddress_t (cStruct): #< permissionType: 0 for deny, 1 for allow; addressFilterType: 0 for range, 1 for mask.; addressRange: ip range for filter when addressFilterType is 0.; addressMask: mask for filter when addressFilterType is 1.
	_fields_ = [('id', CHAR * (MAX_USERNAME_LEN + 1)), ('permissionType', INT), ('addressFilterType', INT), ('addressRange', AddressRange_t), ('addressMask', AddressMask_t)]
class IPFilter2_t (cStruct): #< enabled: 0 for disable, 1 for enable; permissionType: 0 for deny, 1 for allow.; ipfilterAddresses: filter rule list.
	_fields_ = [('enabled', INT), ('permissionType', INT), ('ipfilterAddresses', IPFilterAddress_t * MAX_IPFILTER_NUM)]
class DefaultGateway_t (cStruct):
	_fields_ = [('ipAddress', CHAR * IPADDRESS_LEN), ('ipV6Address', CHAR * IPV6ADDRESS_LEN)]
class DNS_t (cStruct):
	_fields_ = [('ipAddress', CHAR * IPADDRESS_LEN), ('ipV6Address', CHAR * IPV6ADDRESS_LEN)]
class IPAddress_t (cStruct):
	_fields_ = [
		('version', INT), #< ip version, 1 for ipv4, 2 for ipv6, 3 for dual.
		('addressingType', INT), #< ip address type, 1 for static , 2 for dhcp.
		('address', CHAR * IPADDRESS_LEN), ('mask', CHAR * IPADDRESS_LEN), 
		('v6Address', CHAR * IPV6ADDRESS_LEN), 
		('v6Mask', INT), #TODO ipv6 mask is integer, needs to ensure the effective on other code when change it.
		('gateway', DefaultGateway_t), ('primaryDns', DNS_t), ('secondaryDns', DNS_t) 
	]
class NetworkInterface_t (cStruct):
	_fields_ = [('id', CHAR * 8), ('mac', CHAR * (MAC_LEN + 1)), ('ip', IPAddress_t), ('wifi', Wifi_t), ('ipfilter', IPFilter2_t), ('pppoe', PPPoE_t), ('status', INT)]
	@property
	def dhcp(self): return bool(self.ip.addressingType-1)
	@dhcp.setter
	def dhcp(self, is_dhcp=False): self.ip.addressingType = 1 + int(bool(is_dhcp))
	@property
	def ipaddr(self): return self.ip.address
	@ipaddr.setter
	def ipaddr(self, v): self.ip.address = v
	@property
	def ipmask(self): return self.ip.mask
	@ipmask.setter
	def ipmask(self, v): self.ip.mask = v
	@property
	def ipgateway(self): return self.ip.gateway.ipAddress
	@ipgateway.setter
	def ipgateway(self, gateway): self.ip.gateway.ipAddress = gateway[:IPADDRESS_LEN]
	@property
	def dns(self): return [x for x in (self.ip.primaryDns.ipAddress, self.ip.secondaryDns.ipAddress) if x]
	@dns.setter
	def dns(self, v): self.ip.primaryDns.ipAddress, self.ip.secondaryDns.ipAddress = v
class NetworkInterfaceList_t (cStruct):
	_fields_ = [('ifaceList', NetworkInterface_t * NETIFACE_COUNT)]
	@property
	def interfaces(self): return [x for x in self.ifaceList if x.id]
	#TODO: Its not a single value, its list-like object, so need to be careful
	@interfaces.setter
	def interfaces(self, interface):
		for i in range(len(self.ifaceList)):
			if self.ifaceList[i].id == interface.id:
				self.ifaceList[i] = interface
				break
				





class CameraCfg_t (cStruct):
	_fields_ = [
		('iaewbType', INT), #< AEWB_MODE_OFF, AEWB_MODE_AE, AEWB_MODE_AWB, AEWB_MODE_AEWB
		('iPowerLineFrequencyMode', INT), #< 0:FLICKER_NTSC_MOD 1:FLICKER_PAL_MOD
		('iExposurePriority', INT), #< 0:EXPOSUREPRIT_DEFAULT 1:EXPOSUREPRIT_MANUL
		('iExposureValue', INT), #< [0..100]
		('iSaturation', INT), #< [0..100]
		('iBrightness', INT), #< [0..100]
		('iSharpness', INT), #< [0..100]
		('iContrast', INT), #< [0..100]
		('iDayNightFilterType', INT), #< 0:DAYNIGHTFILTER_AUTO 1:DAYNIGHTFILTER_DAY 2:DAYNIGHTFILTER_NIGHT 3:DAYNIGHTFILTER_CUSTOM
		('iAutoIRISEnable', INT), #< 0: AutoIRISDisable 1: AutoIRISEnable
		('iMeter', INT), #<  4:METER_MATRIX, 5:METER_CENTER
		('iWhiteBalanceMode', INT), #< 0:WB_AUTO, 1:WB_OUTDOOR, 2:WB_INDOOR, 3:WB_MANUAL
		('iRedGain', INT), #< [0..100]
		('iBlueGain', INT), #< [0..100]
		('iGreenGain', INT), #< [0..100]
		('iMirrorValue', INT), #< [0..3] 0:flipH ON flipV ON, 1:flipH ON flipV OFF, 2:flipH OFF flipV ON, 3:flipH OFF flipV OFF
		('iNoise', INT), #< [0..100]
		('iBacklight', INT), #0 off,1 on
		('iLightInhibition', INT), #0 off,1 on
		('iWideDynamic', INT), #0 off,1 on
		('iShutter', INT) 
	]
	@property
	def brightness(self): return self.iBrightness
	@brightness.setter
	def brightness(self, v): self.iBrightness = v
	@property
	def daynight(self): return 'auto day night custom'.split()[self.iDayNightFilterType]
	@daynight.setter
	def daynight(self, mode): self.iDayNightFilterType = dict(zip('auto day night custom'.split(), range(4))).get(mode, 0)


class OSDCfg_t (cStruct):
	_fields_ = [
		('osdPosition', INT), #< osd position: 0- top left, 1- bottom left, 2- top right, 3-bottom right, 4- custom xy
		('osdX', INT), #< osd start x pos must >=40
		('osdY', INT), #< osd start y pos must >=40
		('osdColor', INT), #< unused now font color
		('osdFont', INT), #< unused now font type
		('osdSize', INT), #< font size: 0- large, 1- medium, 2-small
		('osdSysInfoEnable', INT), #< 1: enable display system info
		('osdDateEnable', INT), #< 1: enable display data
		('osdDateFormat', INT), #< see eDateFormat
		('osdTimeEnable', INT), #< 1: enable display time
		('osdTimeFormat', INT), #< see eTimeFormat
		('osdUsrTextEnable', INT), #< 1: enable display user defined text
		('osdUsrText', CHAR * (MAX_OSDTXT_LEN + 1)), #< user defined text
		('osdImgEnable', INT), #< 1: enable display logo image
		('imgTransColor', INT), #< unused now
		('osdUserTextX', INT), ('osdUserTextY', INT), ('osdImageX', INT), ('osdImageY', INT), ('osdSysInfoX', INT), ('osdSysInfoY', INT), ('osdDateX', INT), ('osdDateY', INT)]
	@property # 0- top left, 1- bottom left, 2- top right, 3-bottom right, 4- custom xy
	def position(self): return self.osdPosition
	@position.setter
	def position(self, v): self.osdPosition = v
	@property # 0- large, 1- medium, 2-small
	def fontsize(self): return self.osdSize
	@fontsize.setter
	def fontsize(self, v): self.osdSize = v
	@property
	def showdate(self): return bool(self.osdDateEnable)
	@showdate.setter
	def showdate(self, is_show=True): self.osdDateEnable = int(is_show)
	@property
	def showtime(self): return bool(self.osdTimeEnable)
	@showtime.setter
	def showtime(self, is_show=True): self.osdTimeEnable = int(is_show)
	@property
	def showinfo(self): return bool(self.osdSysInfoEnable)
	@showinfo.setter
	def showinfo(self, is_show=True): self.osdSysInfoEnable = int(is_show)
	@property
	def showtext(self): return bool(self.osdUsrTextEnable)
	@showtext.setter
	def showtext(self, is_show=True): self.osdUsrTextEnable = int(is_show)
	@property
	def text(self): return self.osdUsrText
	@text.setter
	def text(self, v): self.osdUsrText = v.decode('utf-8').encode('cp1251')[:MAX_OSDTXT_LEN/2-1]
	@property # 
	def textxy(self): return self.osdUserTextX, self.osdUserTextY
	@textxy.setter
	def textxy(self, xy): 
		if len(xy) == 2: self.osdUserTextX, self.osdUserTextY = xy


class ServerPorts_t (cStruct):
	_fields_ = [
		# short unsigned int <field>;
		('httpPort', UINT), ('httpsPort', UINT), ('ftpSrvPort', UINT), ('rtspPort', UINT), ('tcpPort', UINT) 
	]

class VideoEffect_t (cStruct):
	_fields_ = [ #< [0..100]
		('byBrightness', BYTE), ('byContrast', BYTE), ('bySaturation', BYTE), ('bySharpness', BYTE) 
	]

class CameraTamper_t (cStruct):
	_fields_ = [
		('enable', INT), #< 1: enable; 0:disable
		('duration', INT), #< alarm duaration
		('sensitivity', INT) #< camera tampersensitivity 0: low; 1:medium; 2 high
	]

class DeviceStatus_t (cStruct):
	_fields_ = [
		('iDeviceUpTime', INT), #< running time (seconds)
		('iDiskNum', INT), #< disk count
		('iCUPLoading', INT), #< average cpu loading
		('iMemLoading', INT), #< memory loading
		('iOpenFileHandles', INT) #< opened file count
	]









class Rectangle_t (cStruct):
	_fields_ = [('startx', INT), ('starty', INT), ('width', INT), ('height', INT)]

class TimeInfo_t (cStruct):
	_fields_ = [
		# short int 
		('Year', UINT), #< [1970..]
		('Month', UINT), #< [1..12]
		('Day', UINT), #< [1..31]
		('Hour', UINT), #< [0..59]
		('Minute', UINT), #< [0..59]
		('Second', UINT) #< [0..59]
	]

class SummerTimeInfo_t (cStruct):
	_fields_ = [('month', INT), ('weekNum', INT), ('dayNum', INT), ('Hour', INT), ('Minute', INT)]
class SummerTime_t (cStruct):
	_fields_ = [('enable', INT), ('startTime', SummerTimeInfo_t), ('endTime', SummerTimeInfo_t)]
class TimePoint_t (cStruct): #< Hour   [0..23], Minute [0..59], Second [0..59]
	_fields_ = [('tm_hour', INT), ('tm_min', INT), ('tm_sec', INT)]
class TimeSection_t (cStruct):
	_fields_ = [('bEnable', INT), ('start', TimePoint_t), ('end', TimePoint_t)]
class TimeTable_t (cStruct):
	_fields_ = [('bAllDay', INT * MAX_DAYS), ('section', TimeSection_t * MAX_DAYS * MAX_TIMESEGMENTS)]
class NET_RECORD_CFG (cStruct):
	_fields_ = [('struSched', TimeTable_t), ('uPreRecordLen', UINT), ('uRedundancyLen', UINT), ('uRecordType', UINT)]
class NET_SNAP_CFG (cStruct):
	_fields_ = [('struSched', TimeTable_t), ('uQulity', UINT), ('uFrameRate', UINT), ('uIntervalTime', UINT)]
class NtpCfg_t (cStruct): #< time zone [0..53], sync interval in day, ntp server port, ntp domain name or ip address
	_fields_ = [('bEnable', INT), ('timeZone', INT), ('interval', INT), ('ntpPort', INT), ('ntpServiceName', CHAR * (MAX_HOST_NAME_LEN + 1))]
class TimeCfg_t (cStruct): # <setMode: 0 - manually, 1 - sync with SNTP server; timedata: if setMode is Mannual, fill the time you want to set
	_fields_ = [('setMode', INT), ('autoAdjust', INT), ('ntpserver', NtpCfg_t), ('timedata', TimeInfo_t), ('summertime', SummerTime_t)]



















class UserInfo_t (cStruct): #< userLevel: 0-administrator, 1-operator, 2-user; cfgRight: operation rigth; opRight: configuration right
	_fields_ = [('userLevel', INT), ('szUserName', CHAR * (MAX_USERNAME_LEN + 1)), ('szPassword', CHAR * (MAX_PWD_LEN + 1)), ('cfgRight', UINT), ('opRight', UINT)]
class UserList_t (cStruct): #< count: the count of users
	_fields_ = [('count', INT), ('User', UserInfo_t * MAX_USER_NUM)]

class DDNSCfg_t (cStruct):
	_fields_ = [
		('bEnableDDNS', INT), 
		('hostIndex', INT),  #< host type see
		('szUserName', CHAR * (MAX_USERNAME_LEN + 1)), ('szPassword', CHAR * (MAX_PWD_LEN + 1)), ('szDomainName', CHAR * (MAX_DOMAIN_NAME + 1)), ('port', INT), ('updatePerTime', INT)]

class IPFilterPara_t (cStruct):
	_fields_ = [('ipFilterName', CHAR * (MAX_USERNAME_LEN + 1)), ('startAddr', IPAddr_t), ('endAddr', IPAddr_t), ('iBitMask', INT)]

IPFILTER_NONE = 2
	
class IPFilterEntry_t (cStruct): #< 0: IPFILTER_ALLOW (allowed ip), 1: IPFILTER_DENY (denied ip), 2: IPFILTER_NONE
	_fields_ = [('iPermissionType', INT), ('ipFilterPara', IPFilterPara_t * MAX_IPFILTER_NUM)]
class IPFilter_t (cStruct): #< 0: IPFILTER_ALLOW (allowed ip), 1: IPFILTER_DENY (denied ip), 2: IPFILTER_NONE
	_fields_ = [('enable', INT), ('inUse', INT), ('entry', IPFilterEntry_t * IPFILTER_NONE)]
class MulticastCfg_t (cStruct):
	_fields_ = [('struMulticastIpAddr', IPAddr_t), ('MulticastPort', INT)]



# @brief Information of wifi hot spots.
class WifiInfo_t (cStruct):
	_fields_ = [
		('ssid', CHAR * (MAX_WIFISSID_LEN + 1)), 
		('signal', INT),  #< signal for wifi.
		('connected', INT),  #< whether it is connected.
		('networkType', INT),  #< 0 for infrastructure, 1 for adhoc.
		('channel', INT),  #< 1-14 and 0 for auto.
		('security', WirelessSecurity_t)
	]

class EmailRecv_t (cStruct):
	_fields_ = [('recvEnb', INT), ('szReciever', CHAR * (MAX_EMAILADDR_LEN + 1))]

class SMTPServer_t (cStruct):
	_fields_ = [('szUserName', CHAR * (MAX_USERNAME_LEN + 1)), ('szPassword', CHAR * (MAX_PWD_LEN + 1)), ('szSMTPServer', CHAR * (MAX_DOMAIN_NAME + 1)), ('smtpport', USHORT), ('smtpAuth', INT)]
class MailCfg_t (cStruct): #< iMailInterval: send interval
	_fields_ = [('iMailInterval', INT), ('servers', SMTPServer_t * MAX_EMAILSRV_NUM), ('byAttachment', CHAR), ('byEnableSSL', INT), ('szSender', CHAR * (MAX_EMAILADDR_LEN + 1)), ('emailRecv', EmailRecv_t * MAX_MAIL_RECEIVERS)]
class FileQueryCond_t (cStruct):
	_fields_ = [('iChannel', INT), ('iFileType', INT), ('struStartTime', TimeInfo_t), ('struStopTime', TimeInfo_t)]
class FileInfo_t (cStruct):
	_fields_ = [('iChannel', INT), ('starttime', TimeInfo_t), ('endtime', TimeInfo_t), ('szFilename', CHAR * (MAX_FILENAME_LEN + 1)), ('rectype', INT), ('filesize', ULONGLONG)]
class LogQueryCond_t (cStruct):
	_fields_ = [('chn', INT), ('starttime', TimeInfo_t), ('endtime', TimeInfo_t), ('major', SHORTINT), ('minor', SHORTINT)]
class LogEntry_t (cStruct): #< logtime: log writing time
	_fields_ = [('major', INT), ('minor', INT), ('logtime', TimeInfo_t), ('szUser', CHAR * (MAX_USERNAME_LEN + 1)), ('remoteHostAddr', IPAddr_t), ('alarmInPort', SHORTINT), ('alarmOutPort', SHORTINT), ('channel', INT), ('infoLen', INT), ('szInfo', CHAR * (MAX_LOG_INFO_LEN + 1))]
class FTPCfg_t (cStruct): #< port: default 22; trytime: reconnect times; isRBT: support Resume broken transfer
	_fields_ = [('szServer', CHAR * (MAX_DOMAIN_NAME + 1)), ('port', INT), ('szUsername', CHAR * (MAX_USERNAME_LEN + 1)), ('szPassword', CHAR * (MAX_PWD_LEN + 1)), ('szRemotedir', CHAR * (MAX_LOCATION_LEN + 1)), ('timeout', INT), ('trytime', INT), ('isRBT', INT), ('isAnonymous', INT)]
class VideoCodecCfg_t (cStruct):
	_fields_ = [
		('iStreamIdx', INT),  #< see eStreamindex
		('videoCodec', INT),  #< see eVideoCodec
		('encQuality', INT), 
		('rateControlType', INT),  #< see eRateControlType
		('bitrate', INT),  #< kbit main stream: [100..12000] sub stream:[30..1000]
		('frameRate', INT),  #< [5..25] or [5..30]
		('keyFrameInterval', INT),  #< [25..100]
		('StreamQuality', INT)  #< [0..3] 0:Highest quality; 3:lowest quality
	]

class VideoGlobalCfg_t (cStruct):
	_fields_ = [
		('captureMode', INT),  #< see eVideoCaptureMode
		('SubcaptureMode', INT),  #< see eVideoCaptureMode
		('videoCodec', INT)  #< see eVideoCodec
	]

class VideoOutputCfg_t (cStruct):
	_fields_ = [('EnableBNC', INT)]

class ImgCfg_t (cStruct):
	_fields_ = [
		('imgQuality', INT),  #< [1..7]
		('imgframerate', INT),  #< [1..5]
		('interval', INT)  #< snapshot interval [1..600]
	]

class AudioCfg_t (cStruct):
	_fields_ = [
		('audioSampleRate', INT),  #< sample rate [8000 - 44100]
		('audioCodeType', INT),  #< see eAudioCodec
		('audioBitRate', INT)  #< bitrate bps
	]

class MotionDetection_t (cStruct):
	_fields_ = [
		('enable', INT),  #< enable motion detection
		('sensitivity', INT),  #< see eMDSensitivity
		('width', INT),  #< width of picture
		('height', INT),  #< height of picture
		('regions', INT),  #< num of motion detection area
		('rect', Rectangle_t * MAX_MD_AREAS) #< motion detection area rectangle
	]

class PrivacyMask_t (cStruct):
	_fields_ = [
		('enable', INT),  #< 1: enable; 0: disable
		('width', INT),  #< width of picture
		('height', INT),  #< height of picture
		('regions', INT),  #< num of pravicy mask region
		('rect', Rectangle_t * MAX_PRIVACYMASK_AREAS) #< area rectangle
	]

class SerialPortCfg_t (cStruct):
	_fields_ = [
		('iSerialPortType', INT),  #< 1: rs232  0:rs485
		('iEnabled', INT),  #< 1: enable 0: disable
		('iBaudrate', INT),  #< 0: B1200; 1: B2400; 2: B4800; 3: B9600
		('databits', UCHAR), #< 0: CS8; 1:CS7; 2:CS6; 3:CS5
		('parity', UCHAR), #< 0:none; 1:odd; 2:even
		('stopbits', UCHAR), #< 0:0; 1:1
		('flowctl', UCHAR) #< 0:none; 1:hard; 2:xon:xoff
	]

class VidMediaInfo_t (cStruct):
	_fields_ = [
		('vidType', INT), #< -1: VIDCODEC_INVALID, 0: VIDCODEC_H264, 1: VIDCODEC_MPEG4, 2: VIDCODEC_MJPEG, 3: VIDCODEC_COUNT
		('width', INT),  #< video width
		('height', INT),  #< video height
		('fps', INT),  #< [1-25]
		('len', INT),  #< video meta data length(for h.264, sps and pps; for mp4v, vol)
		('pData', CHAR * 512)
	]
	@property
	def codec(self): return 'invalid h264 mpeg4 mjpeg count'.split()[self.vidType+1]
	@property
	def WxH(self): return {'width': self.width, 'height': self.height}

class VideoFileInfo (cStruct):
	_fields_ = [
		('video_frames', LONG), 
		('time', ULONG), #second
		('reserved', CHAR * 32)
	]

class AudMediaInfo_t (cStruct):
	_fields_ = [
		('audType', INT), #< -1: AUDCODEC_INVALID, 0: AUDCODEC_G711_ULAW, 1: AUDCODEC_G711_ALAW, 2: AUDCODEC_COUNT
		('samplerate', INT),  #< audio sample rate (8000, 44100)
		('bitrate', INT),  #< bit rate (bps)
		('channels', INT),  #< audio channels (1 or 2)
		('len', INT),  #< audio meta data length
		('pData', CHAR * 512)
	]
	@property
	def codec(self): return 'invalid ulaw Alow count'.split()[self.audType+1]

class FileFindCond_t (cStruct):
	_fields_ = [('iChannel', INT), ('uFileType', UINT), ('uFileFormat', UINT), ('bIsLocked', UINT), ('tStartTime', TimeInfo_t), ('tStopTime', TimeInfo_t)]

class FileFindResult_t (cStruct):
	_fields_ = [('ch', INT), ('sFileName', CHAR * 100), ('tStartTime', TimeInfo_t), ('tStopTime', TimeInfo_t), ('uFileSize', UINT), ('bLocked', UINT), ('uFileType', UINT)]

class NetVsProtocal_t (cStruct): #< 0x01: PROTO_I8, 0x02: PROTO_VSIP, 0x04: PROTO_ONVIF, 0x08: PROTO_28181, 0x10: PROTO_P1
	_fields_ = [('protoType', INT), ('szDescribe', CHAR * (MAX_DESCRIPTION_LEN + 1))]
class NetProtoList_t (cStruct):
	_fields_ = [('count', INT), ('protos', NetVsProtocal_t * MAX_NET_PROTO_NUM)]
class NET_IO_OUTCFG (cStruct):
	_fields_ = [('uDefaultStatus', UINT), ('uIOOutStatus', UINT), ('uTimeDelay', UINT), ('uTimePluse', UINT), ('uFreqMulti', UINT), ('uDutyRate', UINT)]









class NET_ALARM_HANDLE (cStruct):
	_fields_ = [('uActionMask', UINT), ('byRelAlarmOut', CHAR * MAX_IOOUT_NUM), ('uDuration', UINT)]
class NET_ALARMIN_CFG (cStruct):
	_fields_ = [('szAlarmInName', CHAR * (MAX_ALARMIN_NAME + 1)), ('uAlarmType', UINT), ('uAlarmEnable', UINT), ('struSched', TimeTable_t), ('handle', NET_ALARM_HANDLE)]
class NET_ALARM_PARAM (cStruct):
	_fields_ = [('uAlarmEnable', UINT), ('struSched', TimeTable_t), ('handle', NET_ALARM_HANDLE)]
class NET_ALARM_MD_CFG (cStruct):
	_fields_ = [('md', MotionDetection_t), ('alarmParam', NET_ALARM_PARAM)]
class NET_ALARM_CAMTAM_CFG (cStruct):
	_fields_ = [('ct', CameraTamper_t), ('alarmParam', NET_ALARM_PARAM)]
class NET_ALARM_IO_CFG (cStruct):
	_fields_ = [('alarmParam', NET_ALARM_PARAM)]
class NET_ALARM_BOOT_CFG (cStruct):
	_fields_ = [('alarmParam', NET_ALARM_PARAM)]
class NET_ALARM_NETBROKEN_CFG (cStruct):
	_fields_ = [('alarmParam', NET_ALARM_PARAM)]
class NET_REC_PACKET_CFG (cStruct):
	_fields_ = [('uPackType', UINT), ('uValue', UINT)]
class NET_SDCARD_PARAM (cStruct):
	_fields_ = [('uOverWrite', UINT), ('uAutoFormat', UINT), ('uSDStatus', UINT), ('uSDVolume', UINT), ('uSDFreeSpace', UINT)]
class NET_UPLOAD_CFG (cStruct):
	_fields_ = [('struSched', TimeTable_t), ('uUploadEnable', UINT), ('uUploadType', UINT)]

NETIFACE_COUNT = 2 #< 0:ethernet, 1:wifi
MAX_WIFISSID_LEN = 32
IPADDRESS_LEN = 16 #< IPv4
MAX_WIFIWEP64KEY_LEN = 64
MAX_WIFIWEP128KEY_LEN = 128
MAX_WIFIWPAKEY_LEN = 63

'''
typedef enum enumNW2AddressingType
{
    NW2_CUSTOM = 0,
    NW2_STATIC = 1,
    NW2_DHCP = 2
} eNW2AddressingType;
#< 0: NW2_CUSTOM, 1: NW2_STATIC, 2: NW2_DHCP


typedef enum enumNW2IfaceStatus
{
    IFACE_UP          = 0x1,
    IFACE_NO_IP       = 0x2,
    IFACE_DHCP_UP     = 0x4,
    IFACE_PPPOE_UP    = 0x8,
    IFACE_IP_CONFLICT = 0x10
} eNW2IfaceStatus;
#< 0x01: IFACE_UP, 0x02: IFACE_NO_IP, 0x04: IFACE_DHCP_UP, 0x08: IFACE_PPPOE_UP, 0x10: IFACE_IP_CONFLICT

'''

class NetIPCfg_t (cStruct):
	_fields_ = [('mac', CHAR * (MAC_LEN + 1)), ('ip', IPAddress_t)]
class AbatchIPCfg_t (cStruct):
	_fields_ = [('ifaceParam', NetIPCfg_t), ('result', INT)]
class TFC_REALPLAY (cStruct):
	# lLinkMode = eTransportType: 0- RTPoverUDP, 1- RTPoverTCP, 2- RTPoverHTTP, 3- TSoverTCP, 4- TSoverUDP
	# lStreamidx = eStreamIdx: 0 - STREAM_IDX_MJPEG, 1 - STREAM_IDX_AUDIO, 2 - STREAM_IDX_VIDEO_MAIN, 3 - STREAM_IDX_VIDEO_SUB, 4 - STREAM_IDX_COUNT
	_fields_ = [('lChannel', LONG), ('lLinkMode', LONG), ('lStreamidx', LONG), ('bWithaudio', BOOL), ('hPlayWnd', HWND), ('csMultiCastIP', PCHAR)]
	def __init__(self, channel=1, link_mode=3, stream_idx=2, with_audio=True, play_wnd=None, multicast_ip=None):
		self.lChannel, self.lLinkMode, self.lStreamidx, self.bWithaudio, self.hPlayWnd, self.csMultiCastIP = LONG(channel), LONG(link_mode), LONG(stream_idx), BOOL(with_audio), HWND(play_wnd or 0), PCHAR(multicast_ip or '')

class NET_REGCALLBACKPARAM (cStruct):
	_fields_ = [
		('sDeviceID', CHAR * MAX_DEVICE_NAME_LEN), 
		('sPassword', CHAR * MAX_PWD_LEN), 
		('sSerialNumber', BYTE * (MAX_SERIAL_NUM + 1)), 
		('dwDeviceType', DWORD), 
		('nStatus', BYTE), 
		('byNetType', BYTE), 
		('byRes', BYTE * 14)
	]
	
class NET_ALARMER (cStruct):
	_fields_ =[
		('byUserIDValid', BYTE), 
		('bySerialValid', BYTE), 
		('byVersionValid', BYTE), 
		('byDeviceNameValid', BYTE), 
		('byMacAddrValid', BYTE), 
		('byLinkPortValid', BYTE), 
		('byDeviceIPValid', BYTE), 
		('bySocketIPValid', BYTE), 
		('lUserID', LONG), 
		('sSerialNumber', BYTE * (MAX_SERIAL_NUM + 1)), 
		('dwDeviceVersion', DWORD), 
		('sDeviceName', CHAR * MAX_DEVICE_NAME_LEN), 
		('byMacAddr', BYTE * MAC_LEN), 
		('wLinkPort', WORD), 
		('sDeviceIP', CHAR * 128), 
		('sSocketIP', CHAR * 128), 
		('byIpProtocol', BYTE), 
		('byRes2', BYTE * 11) 
	]
	
class VideoFormat (cStruct):
	_fields_ = [
		('width', INT), 
		('height', INT), 
		('fps', INT), 
		('bitrate', INT) 
	]

class AudioFormat (cStruct):
	_fields_ = [
		('sampleRate', UINT), 
		('channels', UINT), 
		('bytesPerFrame', UINT), 
		('frameLength', UINT), 
		('bitspersample', UINT), 
	]

#typedef unsigned int fourcc_t;

class MediaFmt (cUnion):
	_fields_ = [
		('audio', AudioFormat),
		('video', VideoFormat)
	]

class MediaInfo (cStruct):
	_fields_ = [
		('i_format', UINT), 
		('MediaFmt', MediaFmt), 
		('duration', INT), 
		('extra', CHAR * 512), 
		('extra_size', INT)
	]

class WATERMARK_INFO (cStruct):
	_fields_ = [
		('pDataBuf', PCHAR), 
		('nSize', LONG), 
		('nFrameNum', LONG), 
		('bRsaRight', BOOL), 
		('nReserved', LONG) 
	]

class FRAME_INFO (cStruct):
	_fields_ = [
		('nWidth', LONG), 
		('nHeight', LONG), 
		('nStamp', LONG), 
		('nType', LONG), 
		('nFrameRate', LONG), 
		('dwFrameNum', DWORD) 
	]






#--- CALLBACKS -------------------------------------------------------------------------------------------

# typedef void (CALLBACK *fDrawFun)(HDC hDc, LONG nUser, int iWidth, int iHeight);
tfc_fDrawFun = cFuncType(None, HDC, LONG, INT, INT)

# typedef LONG (CALLBACK *fREGCallBack)(LONG lUserID, NET_REGCALLBACKPARAM *pRegParam, void *pUser);
tfc_fREGCallBack = cFuncType(LONG, LONG, cPointerType(NET_REGCALLBACKPARAM), PVOID)

# typedef void (CALLBACK *fSearchUnitsCB)(DeviceInfo_t *, DWORD dwUser);
tfc_fSearchUnitsCB = cFuncType(PVOID, cPointerType(DeviceInfo_t), cPointerType(DWORD))

# typedef void (CALLBACK *fExceptionCB)(DWORD dwType, LONG lUserID, LONG lHandle, void *pUser);
tfc_fExceptionCB = cFuncType(None, DWORD, LONG, LONG, PVOID)

# typedef void (CALLBACK *fRealDataCB)(LONG lRealHandle, DWORD dwDataType, BYTE *pBuffer, DWORD dwBufSize, BYTE *extra, DWORD extrelen, DWORD dwUser);
tfc_fRealDataCB = cFuncType(None, LONG, DWORD, cPointerType(BYTE), DWORD, cPointerType(BYTE), DWORD, DWORD)

# typedef void (CALLBACK *fVoiceDataCB)(LONG lVoiceHandle, char *pRecvBuffer, DWORD dwBufSize, BYTE byAudioFlag, void *pUser);
tfc_fVoiceDataCB = cFuncType(None, LONG, PCHAR, DWORD, BYTE, PVOID)

# typedef int (CALLBACK *fUpgradeCB)(int xfered, void *arg);
tfc_fUpgradeCB = cFuncType(cPointerType(INT), INT, PVOID)

# typedef void(CALLBACK *fDownLoadPosCB)(LONG lRealHandle, DWORD dwDataType, BYTE *pBuffer, DWORD dwBufSize, BYTE *extra, DWORD extrelen, DWORD dwUser);
tfc_fDownLoadPosCB = cFuncType(None, LONG, DWORD, cPointerType(BYTE), DWORD, cPointerType(BYTE), DWORD, DWORD)

# typedef void (CALLBACK *fMSGCallBack)(LONG lCommand, NET_ALARMER *pAlarmer, char *pAlarmInfo, DWORD dwBufLen, void *pUser);
tfc_fMSGCallBack = cFuncType(None, LONG, cPointerType(NET_ALARMER), PCHAR, DWORD, PVOID)


