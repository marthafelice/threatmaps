# import dns.resolver
# import sys

# record_types=['A','AAAA','NS','CNAME','MX','PTR','SOA','TXT']
# try:
#     domain=sys.argv[1]
# except IndexError:
#     print('Syntax Error- python demodns.py <domainname>')
#     quit()    
# for records in record_types:
#     try:
#         answer =dns.resolver.resolve(domain,records)
#         print(f'{records} Records')
#         print('-'*50)
#         for ipval in answer:
#             print (ipval.to_text() + '\n')
#     except dns.resolver.NoAnswer:
#         pass
#     except dns.resolver.NXDOMAIN:
#         print(f'{domain} does not exist')
#     except KeyboardInterrupt:
#         print('Goodbye...')
#         quit()
#  import whois
#  print(whois.whois("fortifys.com"))
