import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the CSV
df = pd.read_csv('wikipediaa.csv')

# 2. Convert Time to numeric if needed
df['Time'] = pd.to_numeric(df['Time'], errors='coerce')
df = df.sort_values('Time').reset_index(drop=True)

##############################################################################
# 1) IP Address Distribution (Source vs. Destination) - Improved Readability
##############################################################################
source_counts = df['Source'].value_counts()
dest_counts = df['Destination'].value_counts()
plt.figure(figsize=(10, 5))
width = 0.4  # Width for bars
x = range(len(source_counts.index))
plt.bar(x, source_counts.values, width=width, label='Source IPs', color='steelblue')
plt.bar([i + width for i in x], dest_counts.values, width=width, label='Destination IPs', color='darkorange')
plt.xticks([i + width / 2 for i in x], source_counts.index, rotation=45)
plt.title('IP Address Distribution (Source vs. Destination)')
plt.legend()
plt.tight_layout()
plt.show()

##############################################################################
# 2) TCP Flags Analysis
##############################################################################
flag_counts = df['Flags'].value_counts()
plt.figure(figsize=(8, 5))
plt.bar(flag_counts.index, flag_counts.values, color='green')
plt.title('TCP Flags Distribution')
plt.xlabel('Flags')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

##############################################################################
# 3) TLS Header Fields Analysis
##############################################################################
if 'TLS Server Name' in df.columns and df['TLS Server Name'].notna().any():
    tls_counts = df['TLS Server Name'].value_counts()
    plt.figure(figsize=(8, 5))
    plt.bar(tls_counts.index, tls_counts.values, color='purple')
    plt.title('TLS Server Name Distribution')
    plt.xlabel('TLS Server Name')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
else:
    print("No TLS Server Name data available or column missing.")

##############################################################################
# 4) Packet Size Distribution - Improved Readability
##############################################################################
plt.figure(figsize=(10, 6))
plt.hist(df['Length'], bins=30, color='teal', edgecolor='black', alpha=0.75)
plt.yscale('log')  # Log scale for better visibility of smaller counts
plt.title('Packet Size Distribution')
plt.xlabel('Packet Length (bytes)')
plt.ylabel('Count (log scale)')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

##############################################################################
# 5) Inter-Packet Time Differences
##############################################################################

df['time_delta'] = df['Time'].diff().fillna(0)

df_filtered = df[df['time_delta'] < df['time_delta'].quantile(0.99)].copy()
plt.figure(figsize=(10, 5))
plt.hist(df_filtered['time_delta'], bins=50, color='blue', edgecolor='black', alpha=0.7)

plt.title('Distribution of Inter-Packet Arrival Times')
plt.xlabel('Time Delta (seconds)')
plt.ylabel('Frequency')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

plt.show()

##############################################################################
# 6) Flow Size (Number of Packets per Flow) - Improved Readability
##############################################################################
flow_cols = ['Source', 'Destination', 'Protocol']
if set(flow_cols).issubset(df.columns):
    flow_group = df.groupby(flow_cols)
    flow_size = flow_group.size().reset_index(name='packet_count')
    flow_size_sorted = flow_size.sort_values('packet_count', ascending=False)
    flows = [f"{row['Source']}→{row['Destination']}({row['Protocol']})" for _, row in flow_size_sorted.iterrows()]

    plt.figure(figsize=(10, 6))
    plt.barh(flows, flow_size_sorted['packet_count'], color='darkcyan')
    plt.title('Flow Size Distribution (Number of Packets per Flow)')
    plt.xlabel('Packet Count')
    plt.ylabel('Flow (Src→Dst)')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()
else:
    print("Flow columns (Source, Destination, Protocol) not available.")

##############################################################################
# 7) Flow Volume (Total Bytes per Flow)
##############################################################################
if set(flow_cols).issubset(df.columns) and 'Length' in df.columns:
    flow_volume = flow_group['Length'].sum().reset_index(name='total_bytes')
    flow_volume_sorted = flow_volume.sort_values('total_bytes', ascending=False)
    flows_vol = [f"{row['Source']}→{row['Destination']}({row['Protocol']})" for _, row in flow_volume_sorted.iterrows()]

    plt.figure(figsize=(10, 6))
    plt.barh(flows_vol, flow_volume_sorted['total_bytes'], color='sienna')
    plt.title('Flow Volume Distribution (Total Bytes per Flow)')
    plt.xlabel('Total Bytes')
    plt.ylabel('Flow (Src→Dst)')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()
else:
    print("Flow volume columns or 'Length' not available.")
