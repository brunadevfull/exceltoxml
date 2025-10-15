using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace ExcelXml.Core.Models;

public class ConfigurationModel
{
    [JsonPropertyName("versao")]
    public string Versao { get; set; } = "2.0";

    [JsonPropertyName("ultimaAtualizacao")]
    public DateTime UltimaAtualizacao { get; set; } = DateTime.Now;

    [JsonPropertyName("responsaveis")]
    public List<Responsible> Responsaveis { get; set; } = new();
}
