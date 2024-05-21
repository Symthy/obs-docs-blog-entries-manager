import configparser


# https://zenn.dev/karamawanu/articles/1454bae43fd39f
# セクションの無いiniファイルを読み込むための処置
class ConfigLoader(configparser.ConfigParser):
    def _read(self, fp, fpname):
        def addsection(fp):
            yield "[DEFAULT]"
            yield from fp

        super(ConfigLoader, self)._read(addsection(fp), fpname)
