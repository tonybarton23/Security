import email
from email.policy import default
import re
import ipaddress
import vt
import requests
import json

def find_ipv4(text):
    ipv4_pattern = r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
    return re.findall(ipv4_pattern, text)

def obtain_headers(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            msg = email.message_from_file(file, policy=default)

            headers = {}
            #print(msg.keys())
            headers['receivedHeader'] = str(msg.get_all('Received'))
            headers['receivedSPF'] = str(msg.get_all('Received-spf'))
            headers['returnPathHeader'] = str(msg.get('Return-Path'))
            headers['replyToHeader'] = str(msg.get('Reply-To'))
            headers['fromHeader'] = str(msg.get('From'))
            
            #print(returnPathHeader)
            #print(replyToHeader)
            #print(fromHeader)
            #print(msg.get_all('X-Originating-IP'))

        return headers
    
    except FileNotFoundError:
        print("File not found")

def analyze_from_reply_return(returnPathHeader, replyToHeader, fromHeader):
    #Formating headers to be compared
    returnPathDomain = returnPathHeader.split('@')[1].replace(">", "")
    fromDomain = fromHeader.split('@')[1].replace(">", "")
    if replyToHeader == "None":
        replyToDomain = None
    else:
        replyToDomain = replyToHeader.split('@')[1].replace(">", "")


    #Check to see if return path matches from
    try:
        if returnPathDomain is not None:
            if returnPathDomain == fromDomain:
                print("Return-Path Domain (" + returnPathDomain + ") matches From Domain (" + fromDomain +")")
            else:
                print("Domains do not match")
        else:
            print("Return Path not found")
    except:
        print("Parameters not found")

    #Check to see if reply to matches from
    try:
        if replyToDomain is not None:
            if replyToDomain == fromDomain:
                print("Reply-To header matches From header")
            else:
                print("Domains do not match")
        else:
            print("Reply-To header not found")
    except:
        print("Parameters not found")

def spf_check(receviedSPF):
    spfStatus = receviedSPF.split(" ")[0].replace("['", '')
    print("SPF Status: " + spfStatus)
    receivedSPFIP = str(find_ipv4(headers['receivedSPF'])).split(',')[0].replace("[", '').replace("'", '')
    print(receivedSPFIP)
    return receivedSPFIP
    
def received_order(receivedHeader):
    ipv4_pattern = r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
    receivedIPs = re.findall(ipv4_pattern, headers['receivedHeader'])
    invalidIPs = []
    ip_order = []
    for IP in receivedIPs:
        split_oct = IP.split(".")
        for oct in split_oct:
            if oct[0] == "0":
                if IP in ip_order:
                    #ip_order.remove(IP)
                    invalidIPs.append(IP)
            else:
                if IP not in ip_order:
                    ip_order.append(IP)
                else:
                    continue
    for IP in invalidIPs:
        ip_order.remove(IP)
    print(ip_order)

def connect_vt():
    client = vt.Client('c9c723bb4b55df5438d9d3990ace917f9a6777e4ffbdecfe7acc7f4583ac53ab')

def submit_received_vt(IP):
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{IP}"
    headers = {"accept": "application/json", "x-apikey": 'c9c723bb4b55df5438d9d3990ace917f9a6777e4ffbdecfe7acc7f4583ac53ab'}
    #response = requests.get(url, headers=headers)
    #print(response.json())

    file_path = "data.json"

    try:
        with open(file_path, 'w') as file:
            json.dump(response.json(), file, indent=4)
        print(f"JSON data written to {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

headers = obtain_headers('c:\\PhishingEmails\\[EXTERNAL] Generous Piano Offer.eml')
analyze_from_reply_return(headers['returnPathHeader'], headers['replyToHeader'], headers['fromHeader'])
spf_ip = spf_check(headers['receivedSPF'])
print(spf_ip)
received_order([headers['receivedHeader']])
submit_received_vt(spf_ip)