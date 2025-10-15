using System.Threading.Tasks;

namespace ExcelXml.Desktop.Services;

public interface IFileDialogService
{
    Task<string?> OpenExcelFileAsync();
    Task<string?> SaveXmlFileAsync(string suggestedName);
}
