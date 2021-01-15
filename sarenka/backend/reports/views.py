from rest_framework import views
from pathlib import Path
from json.decoder import JSONDecodeError
from urllib.error import HTTPError
from django.http import HttpResponse
from django.http import FileResponse


from reports.host_info import PDFHostInfo
from reports.hardware_info import PDFHardwareInfo

class GeneratePdfHostInfo(views.APIView):
    def get(self, request, ip_address): 
        pdf = PDFHostInfo()
        pdf.alias_nb_pages()
        pdf.add_page()
        link="http://127.0.0.1:8000/api/censys/"
        pdf.headerOnlyFirstSide(ip_address)
         
        try:
            pdf.chapter(ip_address,link)
        except (JSONDecodeError ,HTTPError) as e :
            return HttpResponse("Something went wrong. Check the ip address and your api key." )
        
        else:
            pdf.set_font('Times', '', 12)
            if not Path('reports/report_host_info.pdf').is_file():
                file_name = Path('reports/report_host_info.pdf')
                file_name.touch(exist_ok=True)  # will create file, if it exists will do nothing
            try:
                pdf.output('reports/report_host_info.pdf', 'F')
                return FileResponse(open('reports/report_host_info.pdf', 'rb'))
            except Exception as ex:
                print("LINIA 30")
                print(type(ex))
                print(ex)


class GeneratePdfHardware(views.APIView):
    """
    Klasa generująca raport w formacie pdf o fizycznym sprzęcie na któym została uruchomiona aplikacja.
    """
    def get(self, request):
        """
        Metoda zwracająca raport w postacie pdf zawięrającym informacje o fizycznym sprzęcie na którym
        :param request: obiket dla widoków Django, przechowujacy informacje o żądania HTTP użytkownika.
        :return: plik pdf
        """
        pdf = PDFHardwareInfo()
        pdf.alias_nb_pages()
        pdf.add_page()
        link="http://127.0.0.1:8000/api/local/hardware"
        pdf.headerOnlyFirstSide()
         
        try:
            pdf.chapter(link)
        except (JSONDecodeError ,HTTPError) as e :
            return HttpResponse("Something went wrong." )
        
        else:
            pdf.set_font('Times', '', 12)
            if not Path('reports/report_hardware_info.pdf').is_file():
                file_name = Path('reports/report_hardware_info.pdf')
                file_name.touch(exist_ok=True)  # will create file, if it exists will do nothing
            try:
                pdf.output('reports/report_hardware_info.pdf', 'F')
                return FileResponse(open('reports/report_hardware_info.pdf', 'rb'))

            except Exception as ex:
                print("LINIA 64")
                print(type(ex))
                print(ex)
