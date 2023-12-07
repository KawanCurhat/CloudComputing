const axios = require('axios');

exports.findNearestPsychologist = async (req, res) => {
  try {
    const { lat, lng } = req.query; // Terima koordinat latitude dan longitude dari permintaan

    const apiKey = 'AIzaSyArR1TI82ofTvWn7lkeOBp_5eGt90-d6og'
    const radius = 5000; // Radius dalam meter (contoh: 5000 meter)
    const type = 'psychologist'; // Jenis tempat yang ingin dicari (psikolog)

    // Membuat panggilan ke Google Places API untuk mencari psikolog terdekat
    const response = await axios.get(`https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=${lat},${lng}&radius=${radius}&type=${type}&key=${apiKey}`);

    // Mengirimkan hasil pencarian sebagai respons
    res.status(200).json(response.data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};
