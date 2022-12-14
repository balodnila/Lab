import click
from Projet_Crawler import crawler


@click.command()
@click.option('--error404', default=False, help='To retrieve only the Error404 links.')
@click.option('--url', help= "Enter the URL you want to crawl")
@click.option('--auth', default=False, help = "To retrieve only the authentication links.")
@click.option('--export',default=False, help = "To export in a csv file the list of links.")


def scan(url, error404,export,auth):
    """
    Scanne et Extrait les données à partir d'une URL
    """
    site_a_scanner = scanner(url)
    site_a_scanner.retrieveAbsoluteAllLinks()
    if error404 :
        site_a_scanner.filterLinks404()
        if export :
            site_a_scanner.exportInCsvFile(site_a_scanner.links_with_error_404)
        else:
            click.echo(site_a_scanner.links_with_error_404)
            print(site_a_scanner.links_with_error_404)
    elif auth :
        site_a_scanner.filterAuthenticate401()
        if export:
            site_a_scanner.exportInCsvFile(site_a_scanner.links_with_authentication_401)
        else:
            print(site_a_scanner.links_with_authentication_401)
    else:
        if export:
            site_a_scanner.exportInCsvFile(site_a_scanner.links_scanned)
        else:
            print(site_a_scanner.links_scanned)
    return

if __name__ == '__main__':
    scan()
