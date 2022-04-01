
from ipaddress import IPv4Address
from ipaddress import IPv4Network

def text_to_csv(filenames, fout='VLANs.csv'):
    """
    Cleans the SolarWinds report from text files and returns CSV for easier reconciliation
    param filenames: list or string of VLANs from Network team SolarWinds report. 
    Ex: ['DC VLANs 12-8-21.txt', 'Branch VLANs 12-8-21.txt'] 
    or 'Branch VLANs 12-8-21.txt'
    param fout: a string of the name of the CSV file returned
    return: none. A CSV is created in the same directory as this script or the location 
    specified if a full path is passed in as out parameter.
    """
    
    filenames = filenames if type(filenames) == list else [filenames]
    splitter = '___________________________________________________________________________'
    with open(fout, 'a') as wf:
        wf.write('VLAN, Description, IP, Subnet, Location, Location IP\n')

    for fname in filenames:
        lines = []
        vlan, desc, ip, subnet, location = [], [], [], [], {'unlocode':[], 'ip':[]}
        with open(fname,'r') as fp:
            for line in fp:
                line = line.strip()
                lines.append(line)
        
        loc = {'unlocode':None, 'ip':None }
        
        
        for i in range(len(lines)):
                
                line = lines[i]
                if line and loc['unlocode'] is None:
                    loc['unlocode'] = line.split(' ')[0]
                    
                    loc['ip'] = (line.split(' ')[1]).strip('():')
                
                if line.startswith('interface'):     
                    dat = line.split(' ')
                    vlan.append(' '.join(_ for _ in dat[1:]))
                    i += 1
                    line = lines[i]
                    
                    if line.startswith('description'):
                        dat = line.split(' ')
                        
                        if len(dat) > 1:
                            desc.append(' '.join(_ for _ in dat[1:]))
                        else:
                            desc.append('none')              
                    
                    else:
                            desc.append('none')
                            
           #----------------------------------------                 
                            
                elif line.startswith('ip address'):
                    dat = line.split(' ')
                    ip.append(dat[2])
                    if len(dat) > 3:
                        subnet.append(dat[3])
                    location['unlocode'].append(loc['unlocode'])
                    location['ip'].append(loc['ip'])
                    
                    
                elif line.startswith('no ip'):
                    ip.append('none')
                    if len(dat) > 3:
                        subnet.append('none')
                    location['unlocode'].append(loc['unlocode'])
                    location['ip'].append(loc['ip'])
                    
                if line == splitter:
                    loc['unlocode'] = None
                    loc['ip'] = None
                
        print('vlan: {} desc: {} ip: {} sub: {} file: {}'.format(len(vlan), len(desc), len(ip), len(subnet), fname))
        
        for i in range(len(vlan)):
            with open(fout, 'a') as wf:
                if len(subnet):
                    wf.write(vlan[i] + ', ' + desc[i] + ', ' + ip[i] + ', ' + subnet[i] + ', ' + location['unlocode'][i] + ', ' + location['ip'][i] + '\n')
                else:
                    wf.write(vlan[i] + ', ' + desc[i] + ', ' + ip[i] + ', ' + ', ' + location['unlocode'][i] + ', ' + location['ip'][i] +'\n')

def compare_ips(f1='disco_results.txt', f2='sw_results.txt', fout=None, batch=5000):
    """
    To be run after list_ips. ONce the lists of all IPs and all IPs in all ranges for SolarWinds and Discovery 
    have been captured through list_ips, 
    this iterates through them and removes the ones in common from the set of SolarWinds IPs. 
    By the end, only IPs in SolarWinds that are not in 
    Discovery are returned through the fout file.
    param f1: string filename for the Discovery IP addresses (single IPs not Ranges)
    param f2: string filename for the SolarWinds IP addresses (single IPs not Ranges)
    param fout: string of path/filename to save results to
    param batch: batch size for processing Discovery IPs. Note: first time list_ips ran, SW had MANY fewer 
    IP addresses total and the Discovery list was ~1GB and could not be processed as a single set due to RAM limits
    return: none. If fout is provided, results are written to the file indicated.
    """
    with open(f2, 'r') as fp2:
        s2 = set([(_.split(',')[0]).strip() for _ in fp2])
        with open(f1, 'r') as fp1:
            s1 = set()
            for i, _ in enumerate(fp1):
                s1.add((_.split(',')[0]).strip())
                if i % batch == 0 and i > 0:
                    s2 = s2 - s1    # if we've seen it in the discovery set (s1), we don't need to keep looking for it!
                    s1 = set()
        fout = fout if fout else f1.split('_')[0] + '_' + f2.split('_')[0] + '_results.txt'
        if fout:
            with open(fout, 'a') as fp:
                for __ in s2:
                    fp.write(__)

def list_ips(fin='disco.txt', save=False, fout=None):
    """
    Converts a text file listing IP addresses AND ranges to return ALL IP addresses in the ranges and IP addresses given. This took ~30 minutes to run for Discovery!
    param fin: string of filename to process. IP addresses and ranges should be on separate lines (ex. take column of IP ranges/address from spreadsheet)
    param save: boolean to save results
    param fout: string of filename to save results to. Make sure save is set to True if you want the results written to the file. If save is True, by default the results are saved to [fin]_results.txt
    return: none. If save is True, the results are written to [fin]_results.txt or the filename provided in fout
    """
    res = []
    if save and not fout:
        fout = fin.split('.')[0] + '_results.txt'
    with open(fin, 'r') as fp:
        for _ in fp:
            _ = _.strip()
            if ((',' in _) or ('-' in _)) and save:
                with open(fout.split('.')[0] + '_failures.txt', 'a') as fp:
                    fp.write('{}\n'.format(_))
            else:
                _ = IPv4Network(_.strip(), strict=False) if '/' in _ else IPv4Address(_.strip())
                res.append(_)
    if save and fout:
        with open(fout, 'a') as fp:
            for _ in res:
                if type(_) == IPv4Network:
                    for ip in _:
                        fp.write('{}, {}\n'.format(ip, _))
                else:
                    fp.write('{}, {}\n'.format(_, _))

def parse_not_in_file(fname, fout='ips_to_disco.txt'):
    """
    Helper function to return list of IP addresses/ranges from SolarWinds not found in Discovery
    param fname: string of filename to process
    param fout: string of filename to save results
    return: none. Results written to fout (default 'ips_to_disco.txt')
    """
    with open(fname, 'r') as fp:
        need = [(_.split(' ')[0]).strip() for _ in fp if 'not in' in _]
        with open(fout, 'a') as fw:
            for _ in need:
                fw.write('{}\n'.format(_))

def reconcile(df, sf, fout='ip_pkg_sw_disco'):
    with open(df,'r') as d:
        disco = [_.strip() for _ in d]

    with open(sf,'r') as s:
        solar = [_.strip() for _ in s]

    with open(fout.split('.')[0] + '.csv', 'a') as w2:
        w2.write('SolarWinds IP, Discovery IP(s)\n')
    for s in solar: 
        try:
            ips = IPv4Network(s, strict=False) if '/' in s else IPv4Address(s)
            ds = []
            for d in disco: 
                try:
                    if '/' in d:
                        ipd = IPv4Network(d, strict=False)  
                        if ips in ipd or ips == ipd:
                            ds.append(d)
                    elif type(ips) == IPv4Address and ipd == ips:
                        ds.append(d)
                except: 
                    print('Failed to process {}'.format(d))
        except: 
            print('Failed to process {}'.format(s))
        with open(fout.split('.')[0] + '_log.txt', 'a') as wf:
            with open(fout.split('.')[0] + '.csv', 'a') as w2:
                if (len(ds) > 0):
                    wf.write('{} in {}\n'.format(s, ','.join(ds)))
                    w2.write('{},{}\n'.format(s, ','.join(ds)))
                else:
                    wf.write('{} not in any Discovery range(s)\n'.format(s))
                    w2.write('{}\n'.format(s,))
                
def csv_to_column(fin='VLANs.csv', c=2, fout=None, skip_header=True):
    """
    Takes a CSV and returns the column specified by the column number (c)
    param fin: string of filename to process
    param c: int of column number to return. The first column is index ZERO and c is 2 by default for processing VLANS.csv from SolarWinds reports.
    param fout: string of filename to optionally save column to
    return: list of the column. If fout, a file with the results is also saved to that path
    """
    col = []
    with open(fin, 'r') as fp:
        for __, _ in enumerate(fp):
            _ = _.split(',')
            if c < 0 or len(_) < c:
                print('Invalid column number, c. Please input a positive integer that does not exceed the number of columns in fin.')
                return None
            if skip_header and __ == 0:
                continue
            col.append(_[c].strip())
    if fout:
        with open(fout, 'a') as fw:
            for _ in col:
                fw.write('{}\n'.format(_))
    return col


if __name__ == '__main__':
    ###################################################################################
    #  UPDATE THE FILENAMES BELOW THEN RUN                                            #
    ###################################################################################
    # discovery = 'disco_new.txt'
    # solarwinds = 'VLANs_2.txt'
    # save_file = 'discovery_solarwinds_reconciled_12132021'
    # reconcile(discovery, solarwinds, save_file)






    ### STEP 1: Convert SolarWinds text report to CSV ###
    ### Parsing most recent SolarWinds reports ###
    # ins = ['DC VLANs 12-8-21.txt', 'Branch VLANs 12-8-21.txt']
    # text_to_csv(ins, 'VLANs_Location.csv')

    ### STEP 2: Get \n separated list of IP addresses/ranges for Discovery and SolarWinds ###
    # disco, column = '', 0
    # dout = disco.split('.')[0] + '_' + str(column) + '.txt'
    # sout = 'VLANs_2.txt'
    # csv_to_column(fout=sout)
    # csv_to_column(fin=disco, c=0, fout=dout, skip_header=True)
    # dout = 'disco.txt'

    ### STEP 3: Reconcile Discovery and SolarWinds reports ###  
    # reconcile(dout, sout, 'results')



    ### Defining some constants for list_ips ###
    # df = 'disco.txt'
    # sf = 'sw.txt'
    # bs = 5000

    ### Testing ipaddress utils ###
    # print(type(IPv4Network('192.0.2.0/24')) == IPv4Network)
    # print(type(IPv4Network('192.0.2.0/28')))
    print(IPv4Network('192.0.2.0/24') in IPv4Network('192.0.2.0/28'))
    # print(IPv4Network('192.0.2.0/24').subnet_of(IPv4Network('192.0.2.0/28')))
    print(IPv4Address('192.0.2.6') in IPv4Network('192.0.2.0/28'))

    ### Identify SolarWinds to Discovery gap ###
    # parse_not_in_file('ip_pkg_sw_disco.txt')
    # compare_ips(save=True)

    ### Listing IPs from ranges ###
    # list_ips(df, save=True)
    # list_ips(sf, save=True)
