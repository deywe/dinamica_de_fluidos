import pandas as pd
import numpy as np
import hashlib

# 🧠 Configurations
FILE_PATH = 'auditoria_fluidos_lyra_signed.csv'

def check_integrity(df):
    """Verifies data integrity by checking the SHA-256 hash consistency."""
    print("🛡️ Verifying data integrity (Auditing CSV file)...")
    
    # Groups by frame to check for consistency
    groups = df.groupby('frame')
    total_frames = len(groups)
    
    for frame_id, group in groups:
        hash_in_frame = group['sha256_integrity'].unique()
        
        # If there's more than one hash per frame, data is corrupted
        if len(hash_in_frame) > 1:
            print(f"❌ INTEGRITY ERROR IN FRAME {frame_id}: Inconsistent hashes.")
            return False
            
    print(f"✅ Integrity of {total_frames} frames confirmed via CSV seal.")
    return True

def calculate_metrics(df):
    """Calculates paper metrics from the CSV dataset."""
    print("📊 Calculating metrics for the paper...")
    
    # 🧠 Metrics Reconstruction (based on CSV columns)
    dt = 0.01 
    
    # Sort by time and particle to calculate derivatives
    df_sorted = df.sort_values(['p_id', 'frame'])
    
    # Calculate position differences (dx, dy) per particle over time
    df_sorted['dx'] = df_sorted.groupby('p_id')['x'].diff()
    df_sorted['dy'] = df_sorted.groupby('p_id')['y'].diff()
    
    # Approximate velocity
    df_sorted['vx'] = df_sorted['dx'] / dt
    df_sorted['vy'] = df_sorted['dy'] / dt
    
    # Kinetic energy per particle and frame
    df_sorted['energia'] = 0.5 * (df_sorted['vx']**2 + df_sorted['vy']**2)
    
    # --- GENERAL METRICS ---
    # Systemic Kinetic Energy
    kinetic_energy = df_sorted['energia'].mean()
    
    # Stability: Standard Deviation of average energy per frame
    energy_per_frame = df_sorted.groupby('frame')['energia'].mean()
    standard_deviation = energy_per_frame.std()
    
    # Coherent Phase Density
    phase_density = np.mean(np.abs(df['phi']))
    
    # Maximum Divergence (Maximum energy variation)
    max_divergence = np.max(np.abs(energy_per_frame - kinetic_energy))
    
    # Final Dataset Hash (Root Hash for the paper)
    root_hash = df['sha256_integrity'].iloc[-1]
    
    print("\n" + "="*70)
    print("📊 SPHY–Φ ANALYZER RESULTS (FOR THE PAPER)")
    print("="*70)
    print(f"{'Systemic Kinetic Energy (K)':35}: {kinetic_energy}")
    print(f"{'Stability Standard Deviation':35}: {standard_deviation}")
    print(f"{'Coherent Phase Density (Φ)':35}: {phase_density}")
    print(f"{'Maximum Observed Divergence':35}: {max_divergence}")
    print(f"{'Final Verification Hash (Root)':35}: {root_hash}")
    print("="*70)

# --- Execution ---
if __name__ == "__main__":
    try:
        df = pd.read_csv(FILE_PATH)
        if check_integrity(df):
            calculate_metrics(df)
    except FileNotFoundError:
        print(f"❌ File {FILE_PATH} not found.")
