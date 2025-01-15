"""
Reference(s):
https://ihateregex.io/expr/ipv6/
"""
import requests as req
import re as regex
import os
import textwrap
import datetime

nl = str("\n")
space = str(" ")
file_name = str("reddit")
line_break = str("#=========\n")
comment = textwrap.dedent("""\
# Title:
# No Reddit (TXT File)
#
# Description:
# Blocks Reddit (simple as that!)                    
#                         
# Compatible with AdAway on Android and multiple ad blockers.
#
# Source(s) Used:
# https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling-porn-social/hosts
#
# Project Home Page:
# https://github.com/ryanbarillos/dns-blocklists
#
""")


# Test
def main():
    # Regular Expressions for IPv4 and IPv6 addresses
    ipv4Regex = regex.compile("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}")
    ipv6Regex = regex.compile("(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))")

    # List of websites
    domains_with_www_prefix=[]
    domains_sans_www_prefix=[]

    
    # Host files to derive my work from
    #
    host_file_sources = ["https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling-porn-social/hosts"]


    """
    STEP 01:

    1. Go through each host file and add fetch their domains
    2. Sort them into the correct domains list defined above
    """
    if os.path.exists(file_name + ".txt"): os.remove(file_name + ".txt")
    
    for host_file in host_file_sources:
        # Grab host file and convert it into list
        #
        domain_list = req.get(host_file).text.split("\n")

        # Separate each URL from its redirect IP address
        # And append them to the corrrect domain lists above
        #
        proceed: bool = False

        for domain in domain_list:
            if (proceed):
                if ipv4Regex.match(domain) or ipv6Regex.match(domain):
                    url = domain.split(" ")
                    # Now to add the domain in the list
                    #
                    if "www." in domain:
                        if domain not in domains_with_www_prefix:
                            domains_with_www_prefix.append(url[1])
                    else:
                        if domain not in domains_sans_www_prefix:
                            domains_sans_www_prefix.append(url[1])
            
            if (domain == "# Reddit"): proceed = True
            if (domain == "" and proceed == True): break

    # Now check if each website has its appropriate counterpart
    # On either list; otherwise, create it
    #
    for domain in domains_sans_www_prefix:
        if domain not in domains_with_www_prefix:
            domains_with_www_prefix.append("www." + domain)

    # Now write to the new hosts file
    #
    file = open(file_name + ".txt", "x")
    file.write(comment)
    file.write("# Last Updated: " + datetime.date.today().strftime("%d %b %Y") + nl) 
    # IPv4 addresses
    #
    file.write("\n\n" + line_break + "IPv4 Nodes\n" + line_break)    
    for domain in domains_sans_www_prefix:
        file.write("0.0.0.0" + space + domain + nl)
    for domain in domains_with_www_prefix:
        file.write("0.0.0.0" + space + domain + nl)
    # IPv6 addresses
    #
    file.write("\n\n" + line_break + "IPv6 Nodes\n" + line_break)    
    for domain in domains_sans_www_prefix:
        file.write("::1" + space + domain + nl)
    for domain in domains_with_www_prefix:
        file.write("::1" + space + domain + nl)
        
# Run script    
main()