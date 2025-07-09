"""
XML generator for Banco do Brasil payment commands
"""

from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
from datetime import datetime
import html

class XMLGenerator:
    """Generate XML files in BB format"""
    
    def __init__(self):
        pass
        
    def generate_xml(self, data, responsible, folha):
        """Generate XML from processed data"""
        # Filter valid records only
        valid_records = [record for record in data if record.get('valid', True)]
        
        if not valid_records:
            raise Exception("Nenhum registro válido encontrado")
            
        # Create root element
        root = Element('ArquivoComandosPagamento')
        
        # Add header information
        self._add_header(root, responsible, folha, len(valid_records))
        
        # Group records by trigrama
        trigrama_groups = self._group_by_trigrama(valid_records)
        
        # Add trigrama list
        lista_trigrama = SubElement(root, 'listaTrigrama')
        
        identificador_counter = 1
        for trigrama_code, records in trigrama_groups.items():
            trigrama_element = SubElement(lista_trigrama, 'trigrama')
            SubElement(trigrama_element, 'trigrama').text = trigrama_code
            
            lista_comandos = SubElement(trigrama_element, 'listaComandosPagamento')
            
            for record in records:
                comando = SubElement(lista_comandos, 'ComandoPagamento')
                
                SubElement(comando, 'identificador').text = str(identificador_counter)
                SubElement(comando, 'matricula').text = record['matricula']
                SubElement(comando, 'alterador').text = 'I'
                SubElement(comando, 'rubrica').text = record['rubrica']
                SubElement(comando, 'tpRubrica').text = record['tipo']
                SubElement(comando, 'formPagto').text = 'AV'
                SubElement(comando, 'valComando').text = record['valor']
                
                identificador_counter += 1
                
        # Convert to string with proper encoding
        return self._format_xml(root)
        
    def _add_header(self, root, responsible, folha, total_records):
        """Add header information to XML"""
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        SubElement(root, 'sistema').text = '3'
        SubElement(root, 'dtGeracao').text = current_time
        SubElement(root, 'dtRemessa').text = current_time
        SubElement(root, 'nome').text = responsible.nome
        SubElement(root, 'cpf').text = responsible.cpf
        SubElement(root, 'perfil').text = responsible.perfil
        SubElement(root, 'tipoPerfilOM').text = responsible.tipo_perfil_om
        SubElement(root, 'nip').text = responsible.nip
        SubElement(root, 'codPapem').text = responsible.cod_papem
        SubElement(root, 'qtdeTotal').text = str(total_records)
        SubElement(root, 'folha').text = folha
        
    def _group_by_trigrama(self, records):
        """Group records by trigrama"""
        groups = {}
        for record in records:
            trigrama = record['trigrama']
            if trigrama not in groups:
                groups[trigrama] = []
            groups[trigrama].append(record)
        return groups
        
    def _format_xml(self, root):
        """Format XML with proper encoding and indentation"""
        # Convert to string
        rough_string = tostring(root, encoding='unicode')
        
        # Parse and format
        parsed = minidom.parseString(rough_string)
        formatted = parsed.toprettyxml(indent="  ", encoding=None)
        
        # Remove extra blank lines
        lines = [line for line in formatted.split('\n') if line.strip()]
        
        # Add XML declaration with correct encoding
        xml_declaration = '<?xml version="1.0" encoding="iso-8859-1" standalone="yes"?>'
        
        # Join lines and replace declaration
        formatted_xml = '\n'.join(lines)
        formatted_xml = formatted_xml.replace('<?xml version="1.0" ?>', xml_declaration)
        
        return formatted_xml
