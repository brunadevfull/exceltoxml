using ExcelXml.Core.Validation;

namespace ExcelXml.Core.Models;

public class Responsible
{
    private string _nome = string.Empty;
    private string _cpf = string.Empty;
    private string _perfil = string.Empty;
    private string _tipoPerfilOm = string.Empty;
    private string _codPapem = "094";
    private string _nip = string.Empty;

    public Responsible()
    {
        DataCadastro ??= DateTime.Now;
        Normalize();
    }

    public Responsible(string nome, string cpf, string nip, string perfil, string tipoPerfilOm)
    {
        Nome = nome;
        Cpf = cpf;
        Nip = nip;
        Perfil = perfil;
        TipoPerfilOm = tipoPerfilOm;
        DataCadastro = DateTime.Now;
        CodPapem = "094";
        Ativo = true;
    }

    public int? Id { get; set; }

    public string Nome
    {
        get => _nome;
        set => _nome = (value ?? string.Empty).Trim().ToUpperInvariant();
    }

    public string Cpf
    {
        get => _cpf;
        set => _cpf = ValidationUtils.CleanCpf(value);
    }

    public string Nip
    {
        get => _nip;
        set => _nip = (value ?? string.Empty).Trim();
    }

    public string Perfil
    {
        get => _perfil;
        set => _perfil = (value ?? string.Empty).Trim().ToUpperInvariant();
    }

    public string TipoPerfilOm
    {
        get => _tipoPerfilOm;
        set => _tipoPerfilOm = (value ?? string.Empty).Trim().ToUpperInvariant();
    }

    public string CodPapem
    {
        get => _codPapem;
        set => _codPapem = string.IsNullOrWhiteSpace(value)
            ? "094"
            : value.Trim().ToUpperInvariant();
    }

    public bool Ativo { get; set; } = true;

    public DateTime? DataCadastro { get; set; } = DateTime.Now;

    public void Normalize()
    {
        Nome = Nome;
        Cpf = Cpf;
        Nip = Nip;
        Perfil = Perfil;
        TipoPerfilOm = TipoPerfilOm;
        CodPapem = CodPapem;
    }
}
