import logging
import click
logger = logging.getLogger('tyrannosaurus')

class Tyrannosaurus:

	@click.command()
	@click.option('--clean', help='Clean up temp files generated by tyrannosaurus')
	def main(self):
		pass

if __name__ == '__main__':
	Tyrannosaurus().main()

__all__ = ['Tyrannosaurus']