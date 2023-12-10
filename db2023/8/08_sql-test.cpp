//#include <boost/spirit.hpp>
#include <boost/spirit/include/classic.hpp>
#include <string>
#include <typeinfo>

namespace VQL
{

  template <typename Iterator>
  auto parse(Iterator begin, Iterator end, bool& success)
  {
    using namespace boost::spirit::x3;

    using x3::lexeme;
    using x3::alpha;
    using x3::phrase_parse;
    using x3::ascii::space;
    using x3::_attr;


    vector<std::string> select;
    std::string from;
    std::string where;
    std::string region;

    auto toSelect = [&](auto & ctx) {select = _attr(ctx);};
    auto toFrom   = [&](auto & ctx) {from   = _attr(ctx);};
    auto toWhere  = [&](auto & ctx) {where  = _attr(ctx);};
    auto toRegion = [&](auto & ctx) {region = _attr(ctx);};


    auto keywords = x3::lit("SELECT") |
      x3::lit("FROM")   |
      x3::lit("WHERE")  |
      x3::lit("REGION");

    auto word     = *(x3::alnum - keywords);
    auto cond     = *(x3::char_ - keywords);


    success = phrase_parse(begin, end,
                           "SELECT" >>
                           (word % ",")[toSelect] >>
                           ("FROM"  >> word[toFrom]) >>
                           -("WHERE" >> x3::lexeme[cond][toWhere]) >>
                           -("REGION" >> word[toRegion])
                           ,
                           space
                           );

    return std::make_tuple(select,from,where,region);


  }



}


int main(int argc, char **argv)
{
  std::string query = "SELECT chr,   pos,chrom FROM variants WHERE chr=3 AND chr=4 REGION exonic";
  bool success = false;

  auto results = VQL::parse(query.begin(), query.end(), success);

  if (success)
    {

      for (auto& field : std::get<0>(results))
	std::cout<<"fields "<<field<<"\n";

      std::cout<<"from "<< std::get<1>(results)<<std::endl;
      std::cout<<"where "<< std::get<2>(results)<<std::endl;
      std::cout<<"region "<< std::get<3>(results)<<std::endl;
      std::cout<<std::flush;

    }
}

