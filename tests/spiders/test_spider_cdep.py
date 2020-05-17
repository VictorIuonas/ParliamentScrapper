import os
from typing import List
from unittest.mock import MagicMock

import scrapy

from items import ParliamentVoteSummaryItem
from spiders.SpiderCDEP import SpidercdepSpider
from tests.test_lib.resources_lib import fake_response_from_file


class TestSpiderCDEP:

    def test_parse_summary(self):
        expected_detailed_vote_info_requests = [
            {
                'url_to_vote_details': 'http://www.cdep.ro/pls/steno/evot2015.nominal?idv=23134&idl=1',
            },
            {
                'url_to_vote_details': 'http://www.cdep.ro/pls/steno/evot2015.nominal?idv=23135&idl=1',
            },
            {
                'url_to_vote_details': 'http://www.cdep.ro/pls/steno/evot2015.nominal?idv=23136&idl=1',
            },
            {
                'url_to_vote_details': 'http://www.cdep.ro/pls/steno/evot2015.nominal?idv=23137&idl=1',
            }
        ]

        scenario = self._Scenario()

        scenario.given_a_request_for_a_vote_summary_page(os.path.join('SpiderCDEP', 'votes_summary.html'))

        scenario.when_sending_the_get_summary_request()

        scenario.then_the_request_data_will_match([MagicMock()])

        scenario.when_parsing_the_page_summary_response()

        scenario.then_the_parse_vote_summary_will_generate_the_requests_for_the_vote_details(
            expected_detailed_vote_info_requests
        )

    def test_parse_vote_details(self):
        preset_item = ParliamentVoteSummaryItem()
        preset_item['url_to_vote_details'] = 'http://www.cdep.ro/pls/steno/evot2015.nominal?idv=23134&idl=1'

        expected_detailed_vote_info_requests = [
            {
                'url_to_vote_details': 'http://www.cdep.ro/pls/steno/evot2015.nominal?idv=23134&idl=1',
                'url_to_transcript': 'http://www.cdep.ro/pls/steno/steno2015.stenograma?ids=8132&idm=5'
            }
        ]

        scenario = self._Scenario()

        scenario.given_a_request_for_a_vote_details(os.path.join('SpiderCDEP', 'vote_details.html'), preset_item)

        scenario.when_parsing_the_vote_details_response()

        scenario.then_the_parse_vote_details_will_generate_the_requests_for_the_vote_transcript(
            expected_detailed_vote_info_requests
        )

    def test_parse_vote_transcript(self):
        expected_vote_information = [
            {
                'transcript': [
                    {
                        'speaker_name': 'Domnul Ion-Marcel Ciolacu',
                        'content': '''Doamnelor și domnilor deputați,
Ordinea de zi și programul de lucru pentru ședința de astăzi, întocmite de Biroul permanent și aprobate de Comitetul liderilor grupurilor parlamentare au fost distribuite.
Pe ordinea de zi avem alegerea vicepreședinților, secretarilor și chestorilor Camerei Deputaților.
Vă reamintesc faptul că, potrivit dispozițiilor regulamentare, cei patru vicepreședinți, patru secretari și patru chestori, care fac parte din Biroul permanent, se aleg la începutul fiecărei sesiuni ordinare.
Repartizarea locurilor în Biroul permanent pentru grupurile parlamentare se aprobă de plenul Camerei Deputaților, la propunerea liderilor grupurilor parlamentare, pe baza negocierilor dintre aceștia, respectându-se configurația politică a Camerei Deputaților.
Biroul permanent a primit documentul întocmit de lideri, în urma negocierilor, iar potrivit acestui document propunerile de repartizare a locurilor de vicepreședinți, secretari și chestori ai Camerei Deputaților se prezintă astfel:
vicepreședinți: Grupul parlamentar al Partidului Social Democrat - două locuri; Grupul parlamentar al PNL - un loc; Grupul parlamentar al USR - un loc;
 secretari: Grupul parlamentar al PSD - două locuri; Grupul parlamentar al PNL - un loc; Grupul parlamentar al minorităților naționale - un loc;
 chestori: Grupul parlamentar al Partidului Social Democrat - un loc; Grupul parlamentar al PNL - un loc; Grupul parlamentar al UDMR - un loc; Grupul parlamentar PRO Europa - un loc. 
Dacă sunt comentarii în legătură cu această repartizare a locurilor pe funcții în Biroul permanent?
Urmează votul asupra propunerilor prezentate.
Vă rog să pregătiţi cartelele de vot. Să înceapă votul.
                        '''
                    },
                    {
                        'speaker_name': 'Domnul Ion-Marcel Ciolacu',
                        'content': '''172 de voturi pentru, 76 de voturi contra, o abținere. Repartizarea locurilor de vicepreședinți, secretari și chestori a fost aprobată.
Vă rog. Domnul Roman, explicarea votului. 
                        '''
                    },
                    {
                        'speaker_name': 'Domnul Florin-Claudiu Roman',
                        'content': '''Mulțumesc, domnule președinte.
Grupul deputaților Partidului Național Liberal a votat împotrivă, pentru că nu se respectă, conform cutumei, ceea ce înseamnă repartizarea locurilor, așa cum spune cutuma, de ani și ani de zile.
Din păcate, continuă această atitudine abuzivă. PSD, practic, astăzi ne-a refuzat dreptul legitim de a mai avea din partea Grupului PNL un membru în Biroul permanent și înțeleg foarte bine care este motivația. Dacă mă uit la Comisia juridică, de exemplu, care nu s-a mai întrunit de o lună și jumătate și practic sunt blocate la nivel de comisii, prin Biroul permanent, tot ceea ce înseamnă inițiative ale Partidului Național Liberal și sunt bombardate toate ordonanțele care vin din zona Guvernului liberal.
O veche vorbă românească spune "Ce ție nu-ți place, altuia nu-i face!". Să vă așteptați și dumneavoastră, ca în momentul în care cetățenii vor stabili o altă majoritate, să primiți un tratament similar.
Chiar nu înțeleg! Speram că va exista un altfel de dialog, o altfel de deschidere. Cât despre un acord al liderilor, așa cum spuneți dumneavoastră, nici nu poate fi vorba. Cel puțin acordul meu scris nu există pe un asemenea document!
Vom vota componența nominală a tuturor grupurilor parlamentare, pentru că noi respectăm regulile parlamentarismului.
Vă mulțumesc. 
                        '''
                    },
                    {
                        'speaker_name': 'Domnul Ion-Marcel Ciolacu',
                        'content': '''Și eu vă mulțumesc.
Domnul lider Simonis. Vă rog. 
                        '''
                    },
                    {
                        'speaker_name': 'Domnul Alfred-Robert Simonis',
                        'content': '''Mulțumesc, domnule președinte.
Stimate coleg,
Ați început spunând că nu se respectă o cutumă de ani și ani de zile și ați continuat prin a spune că se continuă practica abuzivă.
Păi, ori se respecta cutuma până acum și începe o practică, ori... nu înțeleg! Era o cutumă care s-a respectat ani și ani de zile, dar în același timp se continuă o practică?! E foarte complicat.
În ceea ce privește goana dumneavoastră după funcții noi o înțelegem - nu-i nicio surpriză - însă țin să vă reamintesc că ați afirmat faptul că la Comisia juridică nu se lucrează de o lună! Vă reamintesc faptul că de o lună suntem în vacanță parlamentară și era foarte complicat să lucreze, însă vă promit eu că în perioada următoare toate comisiile vor lucra și vom discuta și despre ordonanța de prorogare a termenului de intrare în vigoare a alocațiilor pentru copii, pe care o vom respinge și vă vom obliga să dați alocațiile copiilor, pentru că le așteaptă! (Aplauze.)
Vom discuta despre inițiativa dumneavoastră, de reducere a cotei de TVA, de la 19% la 16%, al cărui inițiator sunteți (Aplauze.) și despre multe alte inițiative care aduc beneficii românilor.
Prin urmare, nu vă faceți griji, vom lucra aplicat și vom face multe lucruri bune în continuare!
Mulțumesc.
(Domnul deputat Florin-Claudiu Roman solicită să ia cuvântul.)
                        '''
                    },
                    {
                        'speaker_name': 'Domnul Ion-Marcel Ciolacu',
                        'content': '''Domnule lider, presupun că pe procedură?! Un minut, da? '''
                    },
                    {
                        'speaker_name': 'Domnul Florin-Claudiu Roman',
                        'content': '''Da!
Mulțumesc.
Sigur, ne-am dori, de exemplu, să întrunim Comisia juridică, să respingem acele modificări pe care le-ați făcut Codurilor de procedură penală, pentru că asta e, dumneavoastră v-a rămas gândul la fostul dumneavoastră șef și înțeleg că nu v-ați rezolvat toate problemele!
În altă ordine de idei, vreau să discutăm și despre Propunerea legislativă de modificare și completare a Legii nr. 115 și a Legii nr. 393 privind statutul aleșilor locali, vrem să discutăm în Parlament alegerea primarilor în două tururi, vrem să discutăm în Parlament Ordonanța nr. 40 privind președinții de consilii județene. Tocmai ați blocat activitatea Comisiei de Cod electoral, căreia i-a expirat mandatul și căreia i-ați prelungit, printr-o propunere a domnului Iordache, care nu era îndrituit să facă această propunere, practic ați blocat tot ce înseamnă voința românilor!
Sigur, fiți convinși că vom plăti alocațiile - că noi le plătim, nu dumneavoastră -, dar mai întâi vom tăia pensiile speciale, ca să putem plăti alocațiile, iar apoi să fiți convinși că vom avea și taxe reduse, pentru că guvernarea liberală înseamnă taxe reduse.
Vă mulțumim dacă votați proiectul nostru! (Vociferări.)
Așa să faceți! 
                        '''
                    }
                ]
            }
        ]

        scenario = self._Scenario()

        scenario.given_a_request_for_a_vote_transcript(os.path.join('SpiderCDEP', 'vote_transcript.html'))

        scenario.when_parsing_the_vote_transcript_response()

        scenario.then_the_parse_vote_transcript_will_extract_it_in_the_result(expected_vote_information)

    class _Scenario:

        def __init__(self):
            self.target = SpidercdepSpider(date='20200203')
            self.actual_summary_requests = None
            self.actual_summary_parse_result = None
            self.actual_parse_details_result = None
            self.actual_parse_transcript_result = None

            self.preset_item = ParliamentVoteSummaryItem()
            self.preset_item['transcript'] = []

            self.response_get_summary = None
            self.response_get_vote_details = None
            self.response_get_vote_transcript = None

        def given_a_request_for_a_vote_summary_page(self, path_to_response_body: str):
            self.response_get_summary = fake_response_from_file(path_to_response_body)

        def given_a_request_for_a_vote_details(
                self, path_to_response_body: str, preset_item: ParliamentVoteSummaryItem
        ):
            self.response_get_vote_details = fake_response_from_file(path_to_response_body)
            self.response_get_vote_details.meta['item'] = preset_item

        def given_a_request_for_a_vote_transcript(self, path_to_response_body: str):
            self.response_get_vote_transcript = fake_response_from_file(path_to_response_body)
            self.response_get_vote_transcript.meta['item'] = self.preset_item

        def when_sending_the_get_summary_request(self):
            self.actual_summary_requests = self.target.start_requests()

        def when_parsing_the_page_summary_response(self):
            self.actual_summary_parse_result = list(self.target.parse_summary(self.response_get_summary))

        def when_parsing_the_vote_details_response(self):
            self.actual_parse_details_result = list(self.target.parse_details(self.response_get_vote_details))

        def when_parsing_the_vote_transcript_response(self):
            self.actual_parse_transcript_result = list(self.target.parse_transcript(self.response_get_vote_transcript))

        def then_the_request_data_will_match(self, expected_requests: List[scrapy.Request]):
            assert len(self.actual_summary_requests) == len(expected_requests)

        def then_the_parse_vote_summary_will_generate_the_requests_for_the_vote_details(
                self, expected_parse_results: List
        ):
            assert len(expected_parse_results) == len(self.actual_summary_parse_result)
            for expected_req, actual_req in zip(expected_parse_results, self.actual_summary_parse_result):
                actual_item = actual_req.meta['item']
                assert expected_req['url_to_vote_details'] == actual_item['url_to_vote_details']

        def then_the_parse_vote_details_will_generate_the_requests_for_the_vote_transcript(
                self, expected_parse_result: List
        ):
            assert len(expected_parse_result) == len(self.actual_parse_details_result)
            for expected_req, actual_req in zip(expected_parse_result, self.actual_parse_details_result):
                actual_item = actual_req.meta['item']

                assert expected_req['url_to_vote_details'] == actual_item['url_to_vote_details']
                assert expected_req['url_to_transcript'] == actual_item['url_to_transcript']

        def then_the_parse_vote_transcript_will_extract_it_in_the_result(self, expected_vote_information: List):
            assert len(expected_vote_information) == len(self.actual_parse_transcript_result)
            for expected_result, actual_result in zip(expected_vote_information, self.actual_parse_transcript_result):
                assert len(expected_result['transcript']) == len(actual_result['transcript'])
                for expected_block, actual_block in zip(expected_result['transcript'], actual_result['transcript']):
                    assert expected_block['speaker_name'] == actual_block['speaker_name']
                    actual_content = actual_block['content'].strip().replace('\n', '').replace('\r', '')
                    expected_content = ' '.join(expected_block['content'].split())
                    assert actual_content == expected_content
