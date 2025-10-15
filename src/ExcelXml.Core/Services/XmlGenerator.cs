using System.Globalization;
using System.Linq;
using System.Text;
using System.Xml;
using System.Xml.Linq;
using ExcelXml.Core.Models;
using ExcelXml.Core.Validation;

namespace ExcelXml.Core.Services;

public class XmlGenerator
{
    public string GenerateXml(IEnumerable<CommandRecord> records, Responsible responsible, string folha)
    {
        if (records is null)
        {
            throw new ArgumentNullException(nameof(records));
        }

        if (responsible is null)
        {
            throw new ArgumentNullException(nameof(responsible));
        }

        if (!ValidationUtils.IsValidFolha(folha))
        {
            throw new ArgumentException("Folha inválida", nameof(folha));
        }

        var validRecords = records.Where(r => r.IsValid).ToList();
        if (validRecords.Count == 0)
        {
            throw new InvalidOperationException("Nenhum registro válido encontrado");
        }

        var timestamp = DateTime.Now.ToString("dd/MM/yyyy HH:mm:ss", CultureInfo.InvariantCulture);

        var document = new XDocument
        {
            Declaration = new XDeclaration("1.0", "iso-8859-1", "yes")
        };

        responsible.Normalize();

        var root = new XElement("ArquivoComandosPagamento",
            new XElement("sistema", "3"),
            new XElement("dtGeracao", timestamp),
            new XElement("dtRemessa", timestamp),
            new XElement("nome", responsible.Nome),
            new XElement("cpf", responsible.Cpf),
            new XElement("perfil", responsible.Perfil),
            new XElement("tipoPerfilOM", responsible.TipoPerfilOm),
            new XElement("nip", responsible.Nip),
            new XElement("codPapem", responsible.CodPapem),
            new XElement("qtdeTotal", validRecords.Count.ToString(CultureInfo.InvariantCulture)),
            new XElement("folha", folha)
        );

        var listaTrigrama = new XElement("listaTrigrama");
        var identificador = 1;

        foreach (var group in validRecords.GroupBy(r => r.Trigrama))
        {
            var trigramaElement = new XElement("trigrama",
                new XElement("trigrama", group.Key)
            );

            var listaComandos = new XElement("listaComandosPagamento");

            foreach (var record in group)
            {
                var comando = new XElement("ComandoPagamento",
                    new XElement("identificador", identificador.ToString(CultureInfo.InvariantCulture)),
                    new XElement("matricula", record.Matricula),
                    new XElement("alterador", "I"),
                    new XElement("rubrica", record.Rubrica),
                    new XElement("tpRubrica", record.Tipo),
                    new XElement("formPagto", "AV"),
                    new XElement("valComando", record.ValorFormatado)
                );

                listaComandos.Add(comando);
                identificador++;
            }

            trigramaElement.Add(listaComandos);
            listaTrigrama.Add(trigramaElement);
        }

        root.Add(listaTrigrama);
        document.Add(root);

        return SerializeDocument(document);
    }

    private static string SerializeDocument(XDocument document)
    {
        var encoding = Encoding.GetEncoding("iso-8859-1");
        var settings = new XmlWriterSettings
        {
            Encoding = encoding,
            Indent = true,
            NewLineChars = "\n",
            NewLineHandling = NewLineHandling.None,
            OmitXmlDeclaration = false
        };

        using var stream = new MemoryStream();
        using (var writer = XmlWriter.Create(stream, settings))
        {
            document.Save(writer);
        }

        return encoding.GetString(stream.ToArray());
    }
}
