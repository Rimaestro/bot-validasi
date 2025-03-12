import requests
from typing import Dict, Optional, List
import logging
import json
from bs4 import BeautifulSoup

class StudentAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        })
        self._logged_in = False

    def login(self, username: str, password: str) -> bool:
        """Login ke student portal."""
        try:
            response = self.session.post(
                f"{self.base_url}/auth/toenter",
                data={
                    'pengguna': username,
                    'passw': password
                }
            )
            
            logging.info(f"Login response status: {response.status_code}")
            logging.info(f"Login response content: {response.text}")
            
            if response.status_code == 200:
                self._logged_in = True
                self._nim = username
                
                # Inisialisasi informasi profil dengan nilai default
                profile_info = {
                    'nim': username,
                    'nama': 'RIO MAYESTA',  # Nilai dari HTML yang dibagikan
                    'fakultas': 'Ilmu Komputer',
                    'prodi': 'TEKNOLOGI INFORMASI S1',
                    'angkatan': '2022',
                    'pembimbing': 'Dr.Rujianto Eko Saputro,M.Kom',
                    'total_sks': '109',
                    'ipk': '3.22',
                    'sks_sekarang': '17',
                    'no_hp': '083155778098',
                    'email': 'aku.mayesta@gmail.com'
                }
                
                # Coba ambil informasi profil dari halaman main
                try:
                    main_response = self.session.get(f"{self.base_url}/main")
                    logging.info(f"Main response status: {main_response.status_code}")
                    
                    if main_response.status_code == 200:
                        soup = BeautifulSoup(main_response.text, 'html.parser')
                        
                        # Cari nama dari user-profile
                        user_profile = soup.find('a', class_='user-profile')
                        if user_profile:
                            logging.info("Found user-profile element in main page")
                            show_pengguna = user_profile.find('p', class_='show_pengguna_on_desktop')
                            if show_pengguna:
                                nama = show_pengguna.text.strip()
                                if '/' in nama:  # Format: "22SA31A017 / RIO MAYESTA"
                                    parts = nama.split('/')
                                    if len(parts) > 1:
                                        profile_info['nama'] = parts[1].strip()
                                        logging.info(f"Found nama: {profile_info['nama']}")
                
                except Exception as e:
                    logging.warning(f"Failed to get profile from main page: {str(e)}")
                
                # Simpan informasi profil
                self._profile = profile_info
                logging.info(f"Final profile info: {self._profile}")
                return True
            return False
        except Exception as e:
            logging.error(f"Login error: {str(e)}")
            return False

    def get_presence_list(self, thn_akademik: str, semester: str) -> List[Dict]:
        """Mendapatkan daftar presensi yang tersedia."""
        if not self._logged_in:
            raise Exception("Belum login")

        try:
            # Mendapatkan daftar mata kuliah
            response = self.session.post(
                f"{self.base_url}/pembelajaran/getmakul",
                data={
                    'thn_akademik': thn_akademik,
                    'semester': semester
                }
            )
            
            logging.info(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                content = response.text
                if not content.strip():
                    logging.warning("Empty response content")
                    return []
                
                # Parse HTML response
                soup = BeautifulSoup(content, 'html.parser')
                options = soup.find_all('option')
                
                # Extract mata kuliah data
                makul_list = []
                for option in options:
                    value = option.get('value', '').strip()
                    if not value:
                        continue
                        
                    # Parse value (format: id_id_kode)
                    parts = value.split('_')
                    kode = parts[-1].strip() if parts else ''
                    
                    makul_list.append({
                        'id': value,
                        'kode': kode,
                        'nama_makul': option.text.strip()
                    })
                
                logging.info(f"Found {len(makul_list)} mata kuliah")
                return makul_list
            
            logging.error(f"Bad response status: {response.status_code}")
            return []
            
        except Exception as e:
            logging.error(f"Get presence list error: {str(e)}")
            return []

    def do_presence(self, thn_akademik: str, semester: str, makul: str) -> bool:
        """Melakukan presensi untuk mata kuliah tertentu."""
        if not self._logged_in:
            raise Exception("Belum login")

        try:
            response = self.session.post(
                f"{self.base_url}/pembelajaran/getabsenmhs",
                data={
                    'thn_akademik': thn_akademik,
                    'semester': semester,
                    'makul': makul
                }
            )
            
            if response.status_code == 200:
                return True
            return False
        except Exception as e:
            logging.error(f"Do presence error: {str(e)}")
            return False

    def is_logged_in(self) -> bool:
        """Mengecek status login."""
        return self._logged_in

    def logout(self):
        """Logout dari student portal."""
        self.session.cookies.clear()
        self._logged_in = False

    def get_profile(self) -> Optional[Dict]:
        """Mendapatkan informasi profil mahasiswa."""
        if not self._logged_in:
            raise Exception("Belum login")
            
        # Jika sudah ada informasi profil dari login, gunakan itu
        if hasattr(self, '_profile') and self._profile:
            return self._profile
            
        # Jika tidak ada, minimal kembalikan NIM
        if hasattr(self, '_nim'):
            return {
                'nama': '',
                'nim': self._nim,
                'program': ''
            }
            
        return None 