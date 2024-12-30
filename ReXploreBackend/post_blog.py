import os
import time
import requests
import dotenv
import mistune

from image import fetch_image

dotenv.load_dotenv()
access_key = os.getenv("ACCESS_KEY")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
refresh_token = os.getenv("REFRESH_TOKEN")
blog_id = os.getenv("BLOG_ID")
imgbb_api_key = os.getenv("IMGBB_API_KEY")

def generate_post_html(title, summary, mindmap, citation):
    title = title.replace("{", r'{').replace("}", r'}')
    summary = summary.replace("{", r'{').replace("}", r'}')
    mindmap = mindmap.replace("{", r'{').replace("}", r'}')
    citation = citation.replace("{", r'{').replace("}", r'}')
    image = fetch_image(title, summary, imgbb_api_key)
    html_summary = mistune.html(summary)
    post = f"""
<div>
<script src="https://cdn.jsdelivr.net/npm/markmap-autoloader@latest"></script>
<style>
.markmap {{
position: relative;
}}
.markmap > svg {{
width: 100%;
border: 2px solid #000;
height: 80dvh;
}}
</style>
<img style='display:block; width:100%;height:100%;' id='paper_image' src='{image}' />
<br>
<p id="paper_summary" data="{summary.replace("&amp;", "&")}">{html_summary.replace("&amp;", "&")}</p>
<br>
<br>
<h2>Mindmap</h2>
<div class="markmap"  id="paper_mindmap" data="# {title} \n {mindmap.replace("&amp;", "&")}">
<script type="text/template">
{mindmap.replace("&amp;", "&")}
</script>
</div>
<br>
<h2>Citation</h2>
<p id="paper_citation" data="{citation.replace("&amp;", "&")}">
{mistune.html(citation.replace("&amp;", "&"))}
</p>
</div>
    """
    return post, image

def create_post(title, category, summary, mindmap, citation):
    post_title = title
    post_category = f"{category}"
    post_body, post_image = generate_post_html(title, summary, mindmap, citation)
    return post_title, post_category, post_body, post_image

def post_post(title, category, body, image):
    data = None
    try:
        data = requests.post(
            url='https://oauth2.googleapis.com/token',
            data={
                'grant_type': 'refresh_token',
                'client_secret': client_secret,
                'refresh_token': refresh_token,
                'client_id': client_id,
            },
            ).json()
        url = f"https://blogger.googleapis.com/v3/blogs/{blog_id}/posts"
        headers = {
            'Authorization': f"Bearer {data['access_token']}",
            "content-type": "application/json"
        }
        post_data = {
            "kind": "blogger#post",
            "blog": {
                "id": blog_id
            },
            "images": [{
                "url": image
            }],
            "title": title,
            "content": body,
            "labels": [category, "ZZZZZZZZZ"]
        }
        data = requests.post(url, headers=headers, json=post_data).json()
        print(data)
        if data['status'] == 'LIVE':
            print(f"The post '{title}' is {data['status']}")
            return True
        else:
            print(f"Error posting {title}: {data}")
            return False
    except Exception as e:
        print(f"Error posting {title}: {e}")
        return False
    
def post_blog(title, category, summary, mindmap, citation, uaccess_key, wait_time=3):
    if uaccess_key != access_key:
        return False
    else:
        status = True
        post_title, post_category, post_body, post_image = create_post(title, category, summary, mindmap, citation)
        status = post_post(post_title, post_category, post_body, post_image)
        print(f"Waiting for {wait_time*60} seconds...")
        time.sleep(wait_time*60)
        if status:
            print('Post created successfully')
            return True
        else:
            print('Failed to create post')
            return False
    
def test(access_key):
    data = {
            "status": "success",
            "Astrophysics": {
                "2412.16344": {
                    "id": "2412.16344",
                    "doi": "https://doi.org/10.48550/arXiv.2412.16344",
                    "title": "Gravitational algebras and applications to nonequilibrium physics",
                    "category": "Astrophysics",
                    "citation": "Grant, C. E., Bautz, M. W., Miller, E. D., Foster, R. F., LaMarr, B., Malonis, A., Prigozhin, G., Schneider, B., Leitz, C., &amp; Falcone, A. D. (2024). Focal Plane of the Arcus Probe X-Ray Spectrograph. ArXiv. https://doi.org/10.48550/ARXIV.2412.16344",
                    "summary": "## Summary\nThe text discusses gravitational algebras and their applications in nonequilibrium physics, specifically in the context of black holes and de Sitter spacetime. It explores the concept of type III and type II von Neumann algebras and their role in understanding the thermodynamic properties of gravitational systems.\n\n## Highlights\n- The Arcus Probe mission concept explores the formation and evolution of clusters, galaxies, and stars.\n- The XRS instrument includes four parallel optical channels and two detector focal plane arrays.\n- The CCDs are designed and manufactured by MIT Lincoln Laboratory (MIT/LL).\n- The XRS focal plane utilizes high heritage MIT/LL CCDs with proven technologies.\n- Laboratory testing confirms CCID-94 performance meets required spectral resolution and readout noise.\n- The Arcus mission includes two co-aligned instruments working simultaneously.\n- The XRS Instrument Control Unit (XICU) controls the activities of the XRS.\n\n## Key Insights\n- The Arcus Probe mission concept provides a significant improvement in sensitivity and resolution over previous missions, enabling breakthrough science in understanding the universe.\n- The XRS instrument's design, including the use of two CCD focal planes and four parallel optical channels, allows for high-resolution spectroscopy and efficient detection of X-ray photons.\n- The CCDs used in the XRS instrument are designed and manufactured by MIT Lincoln Laboratory (MIT/LL), which has a proven track record of producing high-quality CCDs for space missions.\n- The laboratory performance results of the CCID-94 device demonstrate that it meets the required spectral resolution and readout noise for the Arcus mission, indicating that the instrument is capable of achieving its scientific goals.\n- The XRS Instrument Control Unit (XICU) plays a crucial role in controlling the activities of the XRS, including gathering and storing data, and processing event recognition.\n- The Arcus mission's use of two co-aligned instruments working simultaneously allows for a wide range of scientific investigations, including the study of time-domain science and the physics of time-dependent phenomena.\n- The high heritage MIT/LL CCDs used in the XRS focal plane provide a reliable and efficient means of detecting X-ray photons, enabling the instrument to achieve its scientific goals.",
                    "mindmap": "## Arcus Probe Mission Concept\n- Explores formation and evolution of clusters, galaxies, stars\n- High-resolution soft X-ray and UV spectroscopy\n- Agile response capability for time-domain science\n\n## X-Ray Spectrograph (XRS) Instrument\n- Two nearly identical CCD focal planes\n- Detects and records X-ray photons from dispersed spectra\n- Zero-order of critical angle transmission gratings\n\n## XRS Focal Plane Characteristics\n- Frametransfer X-ray CCDs\n- 8-CCD array per Detector Assembly\n- FWHM < 70 eV @ 0.5 keV\n- System read noise ≤ 4 e- RMS @ 625 kpixels/sec\n\n## Detector Assembly\n- Eight CCDs in a linear array\n- Tilted to match curved focal surface\n- Gaps minimized between CCDs\n- Alignment optimized with XRS optics\n\n## Detector Electronics\n- Programmable analog clock waveforms and biases\n- Low-noise analog signal processing and digitization\n- 1 second frame time for negligible pileup\n\n## XRS Instrument Control Unit (XICU)\n- Controls XRS activities and data transfer\n- Event Recognition Processor (ERP) extracts X-ray events\n- Reduces data rate by many orders of magnitude\n\n## CCD X-Ray Performance\n- Measured readout noise 2-3 e- RMS\n- Spectral resolution meets Arcus requirements\n- FWHM < 70 eV at 0.5 keV\n\n## CCID-94 Characteristics\n- Back-illuminated frame-transfer CCDs\n- 2048 × 1024 pixel imaging array\n- 24 × 24 µm image area pixel size\n- 50 µm detector thickness\n\n## Contamination Blocking Filter (CBF)\n- Protects detectors from molecular contamination\n- 45 nm polyimide + 30 nm Al\n- Maintained above +20°C by heater control\n\n## Optical Blocking Filter (OBF)\n- Attenuates visible/IR stray light\n- 40 nm Al on-chip filter\n- Works in conjunction with CBF"
                }
            }
        }
    if data['status'] != 'success':
        print('Failed to fetch data')
    else:
        for category, catdata in data.items():
            if category != 'status':
                for paper_id, paperdata in catdata.items():
                    title = paperdata['title']
                    category = paperdata['category']
                    summary = paperdata['summary']
                    mindmap = paperdata['mindmap']
                    citation = paperdata['citation']
                    access_key = access_key
                    status = post_blog(title, category, summary, mindmap, citation, access_key, 0)
                    print(status)
                    return status
                
if __name__ == '__main__':
    test(access_key)
